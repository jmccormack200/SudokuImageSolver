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
    w, h = source.shape
    bitmap = cv.CreateImageHeader((h, w), cv.IPL_DEPTH_8U, 1)
    cv.SetData(bitmap, source.tostring(), source.dtype.itemsize * h)
    return bitmap
    
    
# init tesseract
api = tesseract.TessBaseAPI()
api.Init(".", "eng", tesseract.OEM_DEFAULT)
api.SetPageSegMode(tesseract.PSM_SINGLE_BLOCK)
api.SetVariable("tessedit_char_whitelist", "123456789")


grid = []
for a in range(1,82):
    imageString = ("output" + str(a) +  ".jpg")
    image = cv2.imread(imageString)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ipl = iplimage_from_array(image)
    tesseract.SetCvImage(ipl, api)
    ocr_text = api.GetUTF8Text()
    #print "line = " + str(a)
    #print ocr_text
    try:
        if ocr_text[0] != " ":
            grid.append(ocr_text[0])
        else:   
            grid.append("0")
    except:
        grid.append("0")
        

      
formattedGrid = []
tempGrid = []
count = 0
for a in grid:
    count += 1
    tempGrid.append(a)
    if count == 9:
        formattedGrid.append(tempGrid)
        tempGrid = []
        count = 0


for a in formattedGrid:
    print a

        
        
        
        
        
        