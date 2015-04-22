import Image
import cv2
import numpy as np
import math
import pylab
import image_slicer
import cv2.cv as cv
import numpy as np
import tesseract
import sudoku
import tessPy #external python file

from matplotlib import pyplot as plt

###############################
#
# Sudoku
#
# Class is instantiated with an image path
# Methods allow for processing of the data
# using the tessPy file. 
#
# instance variables:
# self.image: the image that is opened
#
################################

class Sudoku:
###############################
#
# Initialization
# Inputs: imagepath - path to image
# 
# Outputs: solves the puzzle
#
# All other methods are private methods
#
# Calls main in the tessPy library
################################
    def __init__(self, imagepath):
        self.image = cv2.imread(imagepath)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self._createBox() #Finds the sudoku puzzle in the image
        self._gridSort() #Organizes corners in counter clockwise order
        self._warpGrid() #warps grid to be flat
        self._separteImage() #pulls out each number square
        self._extract() #enhances the squares for processing
        tessPy.main() #call main within tessPy
        
###############################
#
# Create Box
# 
# Private Method
#
# Inputs: none
# 
# Outputs: Draws a box around the largest grid
#          found, this will be the puzzle itself
#          self.gridUnsorted(the coordinates of the corners of the grid)
#
################################    
    def _createBox(self):
        self.laplacian = cv2.Laplacian(self.image, cv2.CV_8U) #First take the laplacian to get edges
        cv2.imwrite("laplacian.jpg", self.laplacian) #save the image, not necessary but used for reporting
        contours, hierarchy = cv2.findContours(self.laplacian, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #find the contours of the image
        biggest = None #used to find the biggest
        max_area = 0 #used to find the largest area
        for i in contours: #iterate over all the contours 
                area = cv2.contourArea(i) #find the area of the contour
                if area > 100: #assume the area will be large to speed up process
                        peri = cv2.arcLength(i,True) #find the length
                        approx = cv2.approxPolyDP(i,0.02*peri,True) #approximates the corners of the polygon
                        if area > max_area and len(approx)==4: #approx should be 4 since it is a square
                                biggest = approx #save the biggest contour
                                max_area = area
        cv2.drawContours(self.image, [biggest], 0, (0,255,0), 3) #draw the contour for visualization purposes
        self.gridUnsorted = biggest #save the grid to be used in the next process
        cv2.imwrite("contours.jpg", self.image)
###############################
#
# Grid Sort
# 
# Private Method
#
# Inputs: none
# 
# Outputs: organizes the grid points in a counter clockwise
#          fashion to allow for the grid to be warped.
#       
#          self.sortedGrid = the sorted grid
################################        
    def _gridSort(self):
        #sort Top Left, Top Right, Bottom Right, Bottom Left
        grid = self.gridUnsorted #load the grid
        
        topLeft = [10000,10000] #initialize locations
        topRight = [0,10000]
        bottomLeft = [10000,0]
        bottomRight = [0,0]
        #organize points
        for point in grid:
            point = point[0]
            if ((self._distance(point)) <= (self._distance(topLeft))):
                topLeft = point
            if (point[0] > topRight[0] and point[1] < topRight[1]):
                topRight = point
            if ((self._distance(point)) >= (self._distance(bottomRight))):
                bottomRight = point
            if (point[0] < bottomLeft[0] and point[1] > bottomLeft[1]):
                bottomLeft = point
            outputgrid = np.array([topLeft, topRight, bottomRight, bottomLeft], np.float32)
        self.sortedGrid = outputgrid #save the grid to self.sortedGrid
###############################
#
# Ditance
# 
# Private Method
#
# Inputs: point
# 
# Outputs: the ditance from point 0,0 in the image to help with
#          locating which corners are located where
################################                 
    def _distance(self, point):
        return math.sqrt(point[0]**2 + point[1]**2)
###############################
#
# Warp Grid
# 
# Private Method
#
# Inputs: none
# 
# Outputs: Transforms the grids perspective to flatten it if it is
#          off axis
#       
################################             
    def _warpGrid(self):
        warpCoordinates = np.array([[0,0],[511,0],[511,511],[0,511]], np.float32) #The ideal corner coordinates
        #find the values needed to transform from the corners we have to the ones we want
        transformValues = cv2.getPerspectiveTransform(self.sortedGrid, warpCoordinates) 
        self.warpImage = cv2.warpPerspective(self.image, transformValues, (512,512)) #warp the iamge
        cv2.imwrite("warpImage.jpg", self.warpImage) #save the image for later
###############################
#
# Separate Image
# 
# Private Method
#
# Inputs: none
# 
# Outputs: separates the image into 81 chunks of equal size
#          since it has been transformed, it pulls out each digit
#          individually
#       
################################         
    def _separteImage(self):
        #image is 512, broken into 9 sections, multipled by -1 to make the math easier
        subdivision = (512/9) * -1 
        #open the image
        imageMat = (self.warpImage)
        pointArray = []
        count = 1
        
        #create an array of the subdivisions for creating the image
        for point in range(511,0,subdivision):
            pointArray.append(point)
        
        #create an empty array
        segmentImage = np.zeros((56,56))
        
        #for each x and y crossing
        for xPoint in range(len(pointArray) - 1):
            for yPoint in range(len(pointArray) - 1):
            #loop over the points and save in a new image
                for x in range(pointArray[xPoint],pointArray[xPoint+1],-1):
                    for y in range(pointArray[yPoint],pointArray[yPoint+1],-1):
                        segmentImage[x - pointArray[xPoint]][y-pointArray[yPoint]] = imageMat[x][y]
                #save image strings for editing
                cv2.imwrite("output" + str(count) + ".jpg", segmentImage)
                #reset
                segmentImage = np.zeros((56,56))
                count += 1
###############################
#
# Extract Image
# 
# Private Method
#
# Inputs: none
# 
# Outputs: enhances the image to improve
#          tesseracts ability to read digits
#       
################################                 
    def _extract(self):
        #for each image
        for a in range(1,82):
            #open the images
            imageString = ("output" + str(a) +  ".jpg")
            image = cv2.imread(imageString)
            #crop the image
            image = image[11:51,11:51]
            #conver the image to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            #apply an adaptive threshold
            binary = cv2.adaptiveThreshold(
                src=gray, maxValue=255,
                adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                thresholdType=cv2.THRESH_BINARY, blockSize=11, C=2)
            #Apply a median blue to remove noise
            blurred = cv2.medianBlur(binary, ksize=5)
            #Unsharp mask
            gBlur = cv2.GaussianBlur(blurred, (5,5), 0)
            sharpened = cv2.addWeighted(binary, 1, gBlur, -2.55, 255)
            #Save image
            cv2.imwrite("output" + str(a) + ".jpg", sharpened)
        

        
if __name__ == "__main__":
    sudoku = Sudoku("sudoku.jpg")
    
