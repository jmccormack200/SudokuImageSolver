import cv2
import cv2.cv as cv
import numpy as np
import tesseract
import sudoku



def iplimage_from_array(source):
    """
    The new Python-OpenCV-Binding cv2 uses numpy arrays as images, while the
    old API uses the same image format (Iplimage) as the c/c++ binding.

    This function can be used to create a Iplimage from a numpy array.
    """
    w, h, z = source.shape
    bitmap = cv.CreateImageHeader((h, w), cv.IPL_DEPTH_8U, 1)
    cv.SetData(bitmap, source.tostring(), source.dtype.itemsize * h)
    return bitmap
    
    
# init tesseract
api = tesseract.TessBaseAPI()
api.Init(".", "eng", tesseract.OEM_DEFAULT)
api.SetPageSegMode(tesseract.PSM_SINGLE_BLOCK)
api.SetVariable("tessedit_char_whitelist", "123456789")



for a in range(1,82):
    imageString = ("output" + str(a) +  ".jpg")
    image = cv2.imread(imageString)
    ipl = iplimage_from_array(image)
    tesseract.SetCvImage(ipl, api)
    ocr_text = api.GetUTF8Text()
    print "letter = " + str(a)  
    print ocr_text