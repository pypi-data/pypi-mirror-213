import cv2
import numpy as np

from metalayer.utils import bbox_max
from PIL import Image

def get_text_blobs(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    sobel_img = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize=11)
    blurred_img = cv2.blur(sobel_img, (41,41))
    _, thresholded = cv2.threshold(blurred_img, 0, 255, cv2.THRESH_OTSU)
    # Image.fromarray(thresholded).show()
    return thresholded


def get_text_bboxes(img):
    blobs = get_text_blobs(img)
    contours, hierarchy = cv2.findContours(blobs, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    bboxes = []
    for contour in contours:
        if cv2.contourArea(contour) < 500:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        bboxes.append([x, y, x+w, y+h])

    bboxes_no_children = []
    for i, bbox1 in enumerate(bboxes):
        has_child = False
        for j, bbox2 in enumerate(bboxes):
            if i != j and bbox1[0] < bbox2[0] and bbox1[1] < bbox2[1] and bbox1[2] > bbox2[2] and bbox1[3] > bbox2[3]:
                has_child = True
                break
        if not has_child:
            bboxes_no_children.append(bbox1)
    return bboxes_no_children

split_points = []
def bbox_reading_order(bboxes, inds=None, vertical=False):
    if inds is None:
        inds = list(range(len(bboxes)))

    if len(inds) <= 1:
        return inds

    inds.sort(key=lambda i: bboxes[i][0 if vertical else 1])
    cursor = bboxes[inds[0]][2 if vertical else 3]  # initial cursor position
    split_idx = 0
    order = []
    for n, i in enumerate(inds[1:]):
        if bboxes[i][0 if vertical else 1] > cursor:
            order.extend(bbox_reading_order(bboxes, inds[split_idx:n+1], not vertical))
            split_idx = n+1

            if vertical:
                split_points.append([(int(cursor), int(min(bboxes[i][1] for i in inds))),
                                     (int(cursor), int(max(bboxes[i][3] for i in inds)))])
            else:
                split_points.append([(int(min(bboxes[i][0] for i in inds)), int(cursor)),
                                     (int(max(bboxes[i][2] for i in inds)), int(cursor))])

        cursor = max(cursor, bboxes[i][2 if vertical else 3])

    if split_idx == 0:
        return inds


    order.extend(bbox_reading_order(bboxes, inds[split_idx:], not vertical))
    return order


def fix_ocr_with_textboxes(img, ocr_results):
    bboxes = get_text_bboxes(img)
    textboxes = [[] for _ in bboxes]
    for (l, t, r, b), text in ocr_results:
        y = (t + b) / 2
        found = False
        for bbox_idx, (x1, y1, x2, y2) in enumerate(bboxes):
            if y1 <= y <= y2 and l < x2 and r > x1:
                if len(text.split(' ')) >= 5:
                    i = int((x1-l)/(r-l) * len(text))
                    j = int((x2-l)/(r-l) * len(text))
                    i = max(0, i)
                    j = min(len(text), j)
                    while i > 0 and text[i] != ' ':
                        i -= 1
                    while j < len(text) and text[j] != ' ':
                        j += 1
                    new_text = text[i:j]
                else:
                    new_text = text
                new_bbox = [
                    max(l, x1),
                    max(t, y1),
                    min(r, x2),
                    min(b, y2)
                ]
                textboxes[bbox_idx].append([new_bbox, new_text])
                found = True
        if not found:
            textboxes.append([[[l, t, r, b], text]])

    extra_bboxes = [tb[0][0] for tb in textboxes[len(bboxes):]]
    # bboxes = [bbox_max(*[b for b, t in tb]) for tb in textboxes[:len(bboxes)] if tb]
    bboxes = [bb for i, bb in enumerate(bboxes) if textboxes[i]]
    textboxes = [tb for tb in textboxes if tb]
    reading_order = bbox_reading_order(bboxes + extra_bboxes)
    textboxes = [textboxes[i] for i in reading_order]
    # flatten using pythons most confusing syntax
    new_results = [ocr_result for textbox in textboxes for ocr_result in textbox]
    return new_results


def test_ocr(img):
    from metalayer.macos.ocr import macos_ocr
    results = macos_ocr(img, paragraph=False)
    text_boxes = get_text_bboxes(img)
    results = fix_ocr_with_textboxes(img, results)
    for bbox, text in results:
        print(text)
        # print('\n***\n')
        # cast bbox [[x1, y1], [x2, y1], [x2, y2], [x1, y2]] to int and draw on img
        x1, y1, x2, y2 = bbox
        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
    for x1, y1, x2, y2 in text_boxes:
        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
    global split_points
    for p1, p2 in split_points:
        # draw horizontal or vertical split lines depending on which direction the split is
        cv2.line(img, p1, p2, (0, 0, 255), 2)

    from PIL import Image
    Image.fromarray(img).show()


if __name__ == '__main__':
    img_path = '/Users/iyevenko/Desktop/ss.png'
    img = cv2.imread(img_path)
    test_ocr(img)
