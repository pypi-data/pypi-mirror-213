import AppKit as ak


def run_applescript(source):
    script = ak.NSAppleScript.alloc().initWithSource_(source)
    res = script.executeAndReturnError_(None)
    if res[1] is not None:
        print(res[1])
    return res[0]


def run_js_in_browser(browser_name, js_code):
    js_code = js_code
    cmd = f'tell application "{browser_name}" to execute in active tab of front window javascript "{js_code}"'
    return run_applescript(cmd)
