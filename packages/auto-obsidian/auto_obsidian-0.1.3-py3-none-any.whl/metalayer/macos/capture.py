import os
import requests
import sys

import AppKit as ak
import Quartz.CoreGraphics as cg
from PIL import Image

sys.path.append('../')
from metalayer import ICON_DIR
from metalayer.utils import slugify, bbox_intersection, bbox_area
from metalayer.cache import WindowCache
from metalayer.macos.utils import cgimage_to_np
from metalayer.macos.applescript import run_applescript, run_js_in_browser

WHITELIST = None
# WHITELIST = ['Google Chrome', 'Discord']
# BLACKLIST = None
BLACKLIST = ['Notification Center', 'Terminal', 'Messages', 'Obsidian']
BLACKLIST += [b + '.app' for b in BLACKLIST]
WINDOW_BLACKLIST = ['Vite + Svelte']
SUPPORTED_BROWSERS = ['Google Chrome']

# Enable Applescript:
# https://christiantietze.de/posts/2020/02/applescript-boilerplate-2020/

# TODO - Problems:
# - Chrome sometimes completely stalls, something to do with applescript
# - OCR works bad on big screen
# - We need to reduce GPT3.5 requests
#     - If text doesn't change much, we should ignore
#     - If you have a terminal output or twitch chat window, we should ignore


window_cache = WindowCache()
def get_windows(save_sites=True):
    # Window list options: https://developer.apple.com/documentation/coregraphics/cgwindowlistoption?language=objc
    window_options = cg.kCGWindowListOptionOnScreenOnly | cg.kCGWindowListExcludeDesktopElements
    window_list = cg.CGWindowListCopyWindowInfo(window_options, cg.kCGNullWindowID)

    windows = []
    seen_bboxes = []
    display_bounds = get_display_bounds()
    for w in window_list:
        if not check_window_valid(w, display_bounds, seen_bboxes):
            continue

        screenshot = render_window(w)
        if screenshot is None:
            continue

        app_name = str(w['kCGWindowOwnerName'])
        window_name = str(w['kCGWindowName'])
        if (app_name, window_name, screenshot) in window_cache:
            print(f'Skipping {app_name} window, already seen in cache')
            continue

        url = None
        icon = None
        if save_sites and app_name in SUPPORTED_BROWSERS:
            url = get_active_url(app_name)
            icon = save_active_favicon(app_name)
            if url is None:
                print('Failed to get URL for window: ', window_name)

        if icon is None:
            pid = int(w['kCGWindowOwnerPID'])
            icon = save_current_app_icon(app_name, pid)

        windows.append({
            'app': app_name,
            'title': window_name,
            'url': url,
            'icon_id': icon,
            'screenshot': screenshot,
        })
        print(f'Saved {app_name} window: {window_name}')
    return windows


def get_display_bounds():
    _, display_ids, _ = cg.CGGetOnlineDisplayList(10, None, None)
    display_bounds = dict()
    for d in display_ids:
        bounds = cg.CGDisplayBounds(d)
        ox = int(bounds.origin.x)
        oy = int(bounds.origin.y)
        h = int(bounds.size.height)
        w = int(bounds.size.width)
        display_bounds[d] = (ox, oy, ox+w, oy+h)
    return display_bounds


def check_window_valid(w, display_bounds, seen_bboxes):
    if WHITELIST and w['kCGWindowOwnerName'] not in WHITELIST:
        return False

    if BLACKLIST and w['kCGWindowOwnerName'] in BLACKLIST:
        return False

    if WINDOW_BLACKLIST and w.get('kCGWindowName') in WINDOW_BLACKLIST:
        return False

    if w['kCGWindowAlpha'] != 1 or w['kCGWindowLayer'] != 0:
        return False

    # Window is not too small
    bounds = w['kCGWindowBounds']
    W = int(bounds['Width'])
    H = int(bounds['Height'])
    if W < 100 or H < 100:
        return False

    # Window is on a display
    on_display = False
    x = int(bounds['X'])
    y = int(bounds['Y'])
    for k, (x1, y1, x2, y2) in display_bounds.items():
        if x1 <= x+W/2 <= x2 and y1 <= y+H/2 <= y2:
            on_display = True
            break
    if not on_display:
        return False

    # Window is <40% contained in another window
    covered = False
    window_bbox = [x, y, x+W, y+H]
    for bbox in seen_bboxes:
        if bbox_area(bbox_intersection(bbox, window_bbox)) > 0.4 * bbox_area(window_bbox):
            covered = True
            break
    if covered:
        return False

    seen_bboxes.append(window_bbox)
    return True


def render_window(window):
    rect = cg.CGRectNull
    window_number = window['kCGWindowNumber']
    only_window = cg.kCGWindowListOptionIncludingWindow
    img_options = cg.kCGWindowImageNominalResolution | cg.kCGWindowImageBoundsIgnoreFraming
    cgimage = cg.CGWindowListCreateImage(rect,
                                         only_window,
                                         window_number,
                                         img_options)
    screenshot = cgimage_to_np(cgimage, flip_channels=True)

    # Black screens
    screenshot_rgb = screenshot[...,:3] * screenshot[...,3:]
    if (screenshot_rgb == 0).sum() / screenshot.size > 0.95:
        return None

    return screenshot


def save_active_favicon(browser_name):
    # Concat with a character that doesn't appear in URL's cause I don't know how to read JS arrays returned through applescript
    # Can also get this stuff by parsing the URL in python but there could be weird edge cases (e.g. port in URL...)
    location_cmd = "location.origin + '|' + location.href"
    res = run_js_in_browser(browser_name, location_cmd)
    if res is None:
        return None
    origin, href = res.stringValue().split('|')

    # Use origin to get filename for favicon and check if already exists
    fname = slugify(origin.split('://')[1]) + '.png'
    fpath = ICON_DIR + fname
    if os.path.exists(fpath):
        return fname[:-4]

    favicon_selector = "document.head.querySelector('link[rel~=icon]').href"
    res = run_js_in_browser(browser_name, favicon_selector)
    path = None if res is None else res.stringValue()

    # Translated from app/extension/contentScript.js
    # If this doesn't work, try using https://pypi.org/project/favicon/
    if path == None:
        path = origin + "/favicon.ico"
    elif path.startswith('//'):
        path = 'https' + path
    elif path.startswith("/"):
        path = origin + path
    elif path.startswith("./"):
        path = origin + '/' + path[2:]
    elif path.startswith(".."):
        d = href
        while path.startswith(".."):
            path = path[3:]
            if d.endswith('/'):
                d = d[:-1]
            d = '/'.join(d.split('/')[:-1])
        path = d + '/'+ path
    elif path.startswith("http"):
        pass
    else:
        path = origin + '/' + path

    try:
        resp = requests.get(path, stream=True, timeout=1)
        assert resp.ok
        img = Image.open(resp.raw)
        img.save(fpath)
        print('Saved favicon found at: ' + path)
    except:
        return None

    return fname[:-4]


def get_active_url(browser_name):
    assert browser_name in SUPPORTED_BROWSERS
    url_cmd = f'tell app "{browser_name}" to get the URL of the active tab of front window'
    res = run_applescript(url_cmd)
    if res is None:
        return None
    url = str(res.stringValue())
    return url


def save_current_app_icon(app_name, pid):
    icon = None
    fname = slugify(app_name) + '.png'
    fpath = ICON_DIR + fname
    if os.path.exists(fpath):
        icon = fname[:-4]
    else:
        app = ak.NSRunningApplication.runningApplicationWithProcessIdentifier_(pid)
        if app is not None:
            icon_img = cgimage_to_np(app.icon().CGImage(), flip_channels=False)
            Image.fromarray(icon_img).save(fpath)
            icon = fname[:-4]
    return icon


if __name__ == '__main__':
    save_active_favicon('Google Chrome')
    print(get_active_url('Google Chrome'))
