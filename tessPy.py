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
    
def getTesseract():    
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
                grid.append(".")
        except:
            grid.append(".")
    
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
  #sampleGrid = ['2', '1', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '3', '1', '.', '.', '.', '.', '9', '4', '.', '.', '.', '.', '7', '8', '2', '5', '.', '.', '4', '.', '.', '.', '.', '.', '.', '6', '.', '.', '.', '.', '.', '1', '.', '.', '.', '.', '8', '2', '.', '.', '.', '7', '.', '.', '9', '.', '.', '.', '.', '.', '.', '.', '.', '3', '1', '.', '4', '.', '.', '.', '.', '.', '.', '.', '3', '8', '.']
  #sampleGrid = ['.', '.', '3', '.', '2', '.', '6', '.', '.', '9', '.', '.', '3', '.', '5', '.', '.', '1', '.', '.', '1', '8', '.', '6', '4', '.', '.', '.', '.', '8', '1', '.', '2', '9', '.', '.', '7', '.', '.', '.', '.', '.', '.', '.', '8', '.', '.', '6', '7', '.', '8', '2', '.', '.', '.', '.', '2', '6', '.', '9', '5', '.', '.', '8', '.', '.', '2', '.', '3', '.', '.', '9', '.', '.', '5', '.', '1', '.', '3', '.', '.']
  sampleGrid = getTesseract()
  printGrid(sampleGrid, 0)
  if hasSolution (sampleGrid):
    printGrid(sampleGrid, 0)
  else: print 'NO SOLUTION'

  
if __name__ == "__main__":
    main()


        
        
        
        
        
        