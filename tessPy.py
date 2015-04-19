import cv2
import cv2.cv as cv
import numpy as np
import tesseract
import sudoku
import re
import random 
import os

# GLOBAL VARIABLES
grid_size = 81

###############################
#
# tessPy
#
# ipLimage_from_array is from tfeIdmann's github
# the Sudoku solver was borrowed from activestate.com
# getTesseract was created by us with help from tfeIdmann's github 
#
# This uses the python tesseract wrapper to
# find the data points and put them in a grid
# 
# Then the puzzle is solved
#
################################


###############################
#
# iplimage from array
#
# Inputs: image array
# 
# Outputs: image array in an old OpenCV
#           format.
#
#   This was needed to get tesseract to be able
#   to use the openCV image.
#
################################
def iplimage_from_array(source):
    """
    This function and information on Tesseract found from:
    https://github.com/tfeldmann/Sudoku
   
    The new Python-OpenCV-Binding cv2 uses numpy arrays as images, while the
    old API uses the same image format (Iplimage) as the c/c++ binding.

    This function can be used to create a Iplimage from a numpy array.
    """
    w, h = source.shape
    bitmap = cv.CreateImageHeader((h, w), cv.IPL_DEPTH_8U, 1)
    cv.SetData(bitmap, source.tostring(), source.dtype.itemsize * h)
    return bitmap
###############################
#
# Get Tesseract
#
# Inputs: none
# 
# Outputs: an array of the sudoku data
#
#   This is where the images are actually processed
#
################################    
def getTesseract():    
    # init tesseract
    api = tesseract.TessBaseAPI()
    #Identify that it is for english
    api.Init(".", "eng", tesseract.OEM_DEFAULT)
    #Set for single block of text
    #Worked better than single character
    api.SetPageSegMode(tesseract.PSM_SINGLE_BLOCK)
    #Only whitelist numbers 1-9
    api.SetVariable("tessedit_char_whitelist", "123456789")


    grid = []
    #iterate for each picture
    for a in range(1,82):
        #open image
        imageString = ("output" + str(a) +  ".jpg")
        image = cv2.imread(imageString)
        #convert to grey
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #convert to the old array type
        ipl = iplimage_from_array(image)
        #Apply the tesseract library
        tesseract.SetCvImage(ipl, api)
        #read the text
        ocr_text = api.GetUTF8Text()
        #print "line = " + str(a)
        #print ocr_text
        try:
            #if a number, save the number
            if ocr_text[0] != " ":
                grid.append(ocr_text[0])
            else:   
                #else mark blank
                grid.append(".")
        except:
            #if error, set as blank
            grid.append(".")
    #return the entire grid
    return grid

'''
Below code borrowed from:
http://code.activestate.com/recipes/578140-super-simple-sudoku-solver-in-python-source-code/
Used to solve grid instead of working from scratch
'''

def isFull (grid):
    return grid.count('.') == 0
  
# can be used more purposefully
def getTrialCelli(grid):
  for i in range(grid_size):
    if grid[i] == '.':
      #print 'trial cell', i
      return i
      
def isLegal(trialVal, trialCelli, grid):

  cols = 0
  for eachSq in range(9):
    trialSq = [ x+cols for x in range(3) ] + [ x+9+cols for x in range(3) ] + [ x+18+cols for x in range(3) ]
    cols +=3
    if cols in [9, 36]:
      cols +=18
    if trialCelli in trialSq:
      for i in trialSq:
        if grid[i] != '.':
          if trialVal == int(grid[i]):
            #print 'SQU',
            return False
  
  for eachRow in range(9):
    trialRow = [ x+(9*eachRow) for x in range (9) ]
    if trialCelli in trialRow:
      for i in trialRow:
        if grid[i] != '.':
          if trialVal == int(grid[i]):
            #print 'ROW',
            return False
  
  for eachCol in range(9):
    trialCol = [ (9*x)+eachCol for x in range (9) ]
    if trialCelli in trialCol:
      for i in trialCol:
        if grid[i] != '.':
          if trialVal == int(grid[i]):
            #print 'COL',
            return False
  #print 'is legal', 'cell',trialCelli, 'set to ', trialVal
  return True

def setCell(trialVal, trialCelli, grid):
  grid[trialCelli] = trialVal
  return grid

def clearCell( trialCelli, grid ):
  grid[trialCelli] = '.'
  #print 'clear cell', trialCelli
  return grid


def hasSolution (grid):
  if isFull(grid):
    #print '\nSOLVED'
    return True
  else:
    trialCelli = getTrialCelli(grid)
    trialVal = 1
    solution_found = False
    while ( solution_found != True) and (trialVal < 10):
      #print 'trial valu',trialVal,
      if isLegal(trialVal, trialCelli, grid):
        grid = setCell(trialVal, trialCelli, grid)
        if hasSolution (grid) == True:
          solution_found = True
          return True
        else:
          clearCell( trialCelli, grid )
      #print '++'
      trialVal += 1
  return solution_found

def printGrid (grid, add_zeros):
  i = 0
  for val in grid:
    if add_zeros == 1:
      if int(val) < 10: 
        print '0'+str(val),
      else:
        print val,
    else:
        print val,
    i +=1
    if i in [ (x*9)+3 for x in range(81)] +[ (x*9)+6 for x in range(81)] +[ (x*9)+9 for x in range(81)] :
        print '|',
    if add_zeros == 1:
      if i in [ 27, 54, 81]:
        print '\n---------+----------+----------+'
      elif i in [ (x*9) for x in range(81)]:
        print '\n'
    else:
      if i in [ 27, 54, 81]:
        print '\n------+-------+-------+'
      elif i in [ (x*9) for x in range(81)]:
        print '\n'
  
  
  
  
def main ():
  sampleGrid = getTesseract() #call our tesseract function
  printGrid(sampleGrid, 0) #apply their sudoku solver
  if hasSolution (sampleGrid): #print if exists, otherwise print no solution
    printGrid(sampleGrid, 0)
  else: print 'NO SOLUTION'

  
if __name__ == "__main__":
    main()


        
        
        
        
        
        