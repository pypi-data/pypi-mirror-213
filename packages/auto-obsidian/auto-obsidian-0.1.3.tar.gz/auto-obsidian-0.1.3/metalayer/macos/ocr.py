# Add macOS imports
import Vision
import cv2
from Foundation import NSData
from Quartz import CGImageCreateWithPNGDataProvider, CGDataProviderCreateWithCFData
from easyocr.utils import get_paragraph

RECOGNITION_LEVEL = Vision.VNRequestTextRecognitionLevelAccurate
USES_LANGUAGE_CORRECTION = True
MINIMUM_TEXT_HEIGHT = 0

# *** GPT-4 Generated ***
def macos_ocr(img, paragraph=True, x_ths=0, y_ths=0.3):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    is_success, buffer = cv2.imencode(".png", img_rgb)
    if not is_success:
        raise ValueError("Failed to convert image to PNG format")

    data = NSData.dataWithBytes_length_(buffer.tobytes(), len(buffer))
    provider = CGDataProviderCreateWithCFData(data)
    cgimage = CGImageCreateWithPNGDataProvider(provider, None, True, 0)

    request = Vision.VNRecognizeTextRequest.new()
    request.setRecognitionLevel_(RECOGNITION_LEVEL)
    request.setUsesLanguageCorrection_(USES_LANGUAGE_CORRECTION)
    request.setMinimumTextHeight_(MINIMUM_TEXT_HEIGHT)
    request.setRevision_(2)

    handler = Vision.VNImageRequestHandler.alloc().initWithCGImage_options_(cgimage, None)

    success, error = handler.performRequests_error_([request], None)
    if not success:
        raise ValueError(f"macOS OCR request failed: {error}")

    results = []
    for result in request.results():
        text = str(result.text()).replace('\n', ' ')
        rect = result.boundingBox()
        x, y, w, h = rect.origin.x, rect.origin.y, rect.size.width, rect.size.height
        # Have to flip y-axis for some reason
        x1 = int(x * img.shape[1])
        y1 = int((1-(y+h*1.0)) * img.shape[0])
        x2 = int((x+w*1) * img.shape[1])
        y2 = int((1-(y-h*0.0)) * img.shape[0])
        results.append([[
            [x1, y1], [x2, y1], [x2, y2], [x1, y2]
        ], text])

    # Use easyocr paragraph grouping
    if paragraph:
        results = get_paragraph(results, mode='ltr', x_ths=x_ths, y_ths=y_ths)
    results = [[[x1, y1, x2, y2], text] for [[x1, y1], [x2, y1], [x2, y2], [x1, y2]], text in results]
    return results


def test_ocr(img, paragraph=True):
    results = macos_ocr(img, paragraph=paragraph)
    for bbox, text in results:
        print(text)
        # print('\n***\n')
        # cast bbox [[x1, y1], [x2, y1], [x2, y2], [x1, y2]] to int and draw on img
        bbox = [[int(x), int(y)] for x, y in bbox]
        cv2.rectangle(img, tuple(bbox[0]), tuple(bbox[2]), (0, 255, 0), 2)
    from PIL import Image
    Image.fromarray(img).show()

if __name__ == '__main__':
    img_path = '/Users/iyevenko/Desktop/paper_img_full.png'
    img = cv2.imread(img_path)
    # test_ocr(img)
    test_ocr(img, paragraph=False)
