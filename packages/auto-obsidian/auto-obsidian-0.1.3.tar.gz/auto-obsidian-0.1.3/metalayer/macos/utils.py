import Quartz.CoreGraphics as cg
import numpy as np
import cv2 as cv


def cgimage_to_np(cg_image, flip_channels=True):
    width = cg.CGImageGetWidth(cg_image)
    height = cg.CGImageGetHeight(cg_image)
    bytesperrow = cg.CGImageGetBytesPerRow(cg_image)

    pixeldata = cg.CGDataProviderCopyData(cg.CGImageGetDataProvider(cg_image))
    image = np.frombuffer(pixeldata, dtype=np.uint8)
    # This is the only way to ensure that the bytes get packed into the image correctly
    # In the worst case, you might lose a row of pixels but at least it doesn't overflow
    image = image[:height*bytesperrow]
    image = image.reshape((height, bytesperrow//4, 4))
    image = image[:,:width,:]
    if flip_channels:
        image = cv.cvtColor(image, cv.COLOR_BGRA2RGBA)
    return image
