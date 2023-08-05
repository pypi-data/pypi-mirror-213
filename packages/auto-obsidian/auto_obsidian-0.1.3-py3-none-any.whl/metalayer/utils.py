import unicodedata
import re

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '_', value).strip('_')

def get_page_id(app, title):
    prefix = slugify(app) + '-' + slugify(title)
    prefix = prefix[:200]   # Keep a safe distance from the 255 char filename limit
    return prefix


def timed(message_format):
    def decorator(func):
        def wrapper(*args, **kwargs):
            import time
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print(message_format.format(end - start))
            return result
        return wrapper
    return decorator


def bbox_area(bbox):
    lx, ly, rx, ry = bbox
    return (ry - ly) * (rx - lx)


def bbox_intersection(bbox1, bbox2):
    lx1, ly1, rx1, ry1 = bbox1
    lx2, ly2, rx2, ry2 = bbox2
    x1, y1, x2, y2 = (max(lx1, lx2), max(ly1, ly2), min(rx1, rx2), min(ry1, ry2))
    if x1 >= x2 or y1 >= y2:
        return [0, 0, 0, 0]
    return [x1, y1, x2, y2]


def bbox_max(*bboxes):
    if len(bboxes) == 0:
        return [0, 0, 0, 0]
    min_lx = min(bb[0] for bb in bboxes)
    min_ly = min(bb[1] for bb in bboxes)
    max_rx = max(bb[2] for bb in bboxes)
    max_ry = max(bb[3] for bb in bboxes)
    return [min_lx, min_ly, max_rx, max_ry]


def test_prefix():
    app = "Google Chrome"
    window = "spotify/annoy: Approximate Nearest Neighbors in C++/Python optimized for memory usage and loading/saving to disk"

    print(get_page_id(app, window))


if __name__ == '__main__':
    #test slugify
    print(slugify('UX Research: Visualization 5 - Google Docs 🔊'))
