import easyocr
import numpy as np
from PIL import Image

from metalayer.ocr_heuristics import fix_ocr_with_textboxes

# import os
# os.environ['OMP_NUM_THREADS'] = '8'

# https://www.jaided.ai/easyocr/documentation/
EASY_OCR_PARAMS = {
    ### TEXT DETECTION PARAMS ###
    'text_threshold': 0.8,  # Text confidence threshold
    'low_text': 0.4,        # Text low-bound score
    'link_threshold': 0.4,  # Link confidence threshold
    'canvas_size': 2560,    # Maximum image size. Image bigger than this value will be resized down.
    'mag_ratio': 1,         # Image magnification ratio
    ### BOUNDING BOX MERGING PARAMS ###
    'slope_ths': 0.5,       # Maximum slope (delta y/delta x) to considered merging. Low value means tiled boxes will not be merged.
    'ycenter_ths': 0.5,     # Maximum shift in y direction. Boxes with different level should not be merged.
    'height_ths': 0.5,      # Maximum different in box height. Boxes with very different text size should not be merged.
    'width_ths':  0.7,       # Maximum horizontal distance to merge boxes
    'add_margin': 0.1,      # Extend bounding boxes in all direction by certain value. This is important for language with complex script (E.g. Thai)
    'x_ths': 0,           # Maximum horizontal distance to merge text boxes when paragraph=True.
    'y_ths': 0.3            # Maximum vertical distance to merge text boxes when paragraph=True
}


class OCR():
    def __init__(self, backend, fix_ocr=True):
        self.fix_ocr = fix_ocr
        if backend not in ['macos', 'easyocr']:
            raise ValueError(f'Unsupported backend: {backend}')

        if backend == 'macos':
            self.reader = None
            from metalayer.macos.ocr import macos_ocr
            self.macos_ocr = macos_ocr
        else:
            self.reader = easyocr.Reader(['en'], gpu=False, detect_network="craft", recog_network='standard')
        self.backend = backend

    def __call__(self, img, paragraph=True):
        if img.shape[2] == 4:
            img[img[:,:,3] == 0] = 0
            img = img[:,:,:3]

        if self.backend == 'macos':
            results = self.macos_ocr(img, paragraph=paragraph, x_ths=EASY_OCR_PARAMS['x_ths'], y_ths=EASY_OCR_PARAMS['y_ths'])
        else:
            results = self.reader.readtext(img, paragraph=paragraph, **EASY_OCR_PARAMS)
            # easyocr combines lines within the same paragraph with newlines, but we want full sentences, so we need spaces
            results = [
                [[res[0][0][0], res[0][0][1], res[0][2][0], res[0][2][1]], res[1].replace('\n', ' ')]
                for res in results
            ]
        if self.fix_ocr and not paragraph:
            results = fix_ocr_with_textboxes(img, results)
        return results


def test_image(image_path, backend):
    import cv2
    import numpy as np
    from PIL import Image

    img = cv2.imread(image_path)
    # get upper middle half of image
    # img = img[:img.shape[0]//2, img.shape[1]//4:img.shape[1]//4*3, :3]
    img = np.bitwise_not(img[...,:3])
    cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)

    results = OCR(backend)(img, paragraph=False)

    for bbox, text in results:
        cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
        print(bbox[:2], text)

    Image.fromarray(img).show()

if __name__ == '__main__':
    img_path = '/Users/iyevenko/Desktop/math.PNG'
    # test_image(img_path, 'easyocr')
    # print('\n***\n')
    test_image(img_path, 'macos')
