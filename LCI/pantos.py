import cv2
try:
    from google.colab.patches import cv2_imshow
except:
    pass
import pandas as pd
import numpy as np
from tqdm import tqdm


def erase_txt(image, blur = True):
    """
    Process an image by either blurring or covering text regions with black rectangles.

    This function takes an image.
    If text with a probability greater than 0.5 is detected, it applies blurring or covers
    the text with a black rectangle. If no such text is found, it returns the original image.

    Args:
        img (numpy.ndarray): The input image to be processed.
        blur (bool, optional): If True, blur the detected text regions; otherwise, cover
                               them with black rectangles. Default is True.

    Returns:
        numpy.ndarray: The processed image.

    Example:
        img = cv2.imread("image.jpg")
        processed_img = proc_img(img, blur=True)
    """
    try:
        from easyocr import Reader
    except:
        import LCI.utils as utl
        utl.install_package('easyocr')
        #!pip install easyocr
        from easyocr import Reader
    try:
        reader = Reader(['es','en'],gpu = True)
    except:
        reader = Reader(['es','en'],gpu = False)
    img = image.copy()
    res = reader.readtext(img)
    # For each results:
    for (bbox, text, prob) in res:
      # The next line display the text along with its associated probability.
      #print("[INFO] {:.4f}: {}".format(prob, text))
      if prob>0.5:
        (tl, tr, br, bl) = bbox
        tl = (int(tl[0]), int(tl[1]))
        tr = (int(tr[0]), int(tr[1]))
        br = (int(br[0]), int(br[1]))
        bl = (int(bl[0]), int(bl[1]))
        
        if blur:
            img[tl[1]:bl[1], tl[0]:tr[0]] = cv2.blur(img[tl[1]:bl[1], tl[0]:tr[0]] ,(53,53))
        else:
            # A fix is needed because the zone that is blur is different from the black rectangle
            img[tl[1]:bl[1], tl[0]:tr[0]] = cv2.rectangle(img[tl[1]:bl[1], tl[0]:tr[0]], tl, br, (0, 0, 0), -1)
    return img