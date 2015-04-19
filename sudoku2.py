import Image
import cv2
import numpy as np
import math
import pylab
import image_slicer
from matplotlib import pyplot as plt

class Sudoku:
    
    def __init__(self, imagepath):
        self.image = cv2.imread(imagepath)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self._createBox()
        self._gridSort()
        self._warpGrid()
        self._separteImage()
        self._extract()

    
    def _createBox(self):
        self.laplacian = cv2.Laplacian(self.image, cv2.CV_8U)
        cv2.imwrite("laplacian.jpg", self.image)
        contours, hierarchy = cv2.findContours(self.laplacian, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        biggest = None
        max_area = 0
        for i in contours:
                area = cv2.contourArea(i)
                if area > 100:
                        peri = cv2.arcLength(i,True)
                        approx = cv2.approxPolyDP(i,0.02*peri,True)
                        if area > max_area and len(approx)==4:
                                biggest = approx
                                max_area = area
        cv2.drawContours(self.image, [biggest], 0, (0,255,0), 3)
        self.gridUnsorted = biggest
        cv2.imwrite("contours.jpg", self.image)
        
    def _gridSort(self):
        #sort Top Left, Top Right, Bottom Right, Bottom Left
        grid = self.gridUnsorted
        
        topLeft = [10000,10000]
        topRight = [0,10000]
        bottomLeft = [10000,0]
        bottomRight = [0,0]
        #print grid
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
        self.sortedGrid = outputgrid
            
    def _distance(self, point):
        return math.sqrt(point[0]**2 + point[1]**2)
        
    def _warpGrid(self):
        warpCoordinates = np.array([[0,0],[511,0],[511,511],[0,511]], np.float32)
        transformValues = cv2.getPerspectiveTransform(self.sortedGrid, warpCoordinates)
        self.warpImage = cv2.warpPerspective(self.image, transformValues, (512,512))
        cv2.imwrite("warpImage.jpg", self.warpImage)
        
    def _separteImage(self):
        subdivision = (512/9) * -1
        imageMat = (self.warpImage)
        pointArray = []
        count = 1
        
        for point in range(511,0,subdivision):
            pointArray.append(point)
        
        segmentImage = np.zeros((56,56))
        
        for xPoint in range(len(pointArray) - 1):
            for yPoint in range(len(pointArray) - 1):
                for x in range(pointArray[xPoint],pointArray[xPoint+1],-1):
                    for y in range(pointArray[yPoint],pointArray[yPoint+1],-1):
                        segmentImage[x - pointArray[xPoint]][y-pointArray[yPoint]] = imageMat[x][y]
                cv2.imwrite("output" + str(count) + ".jpg", segmentImage)
                segmentImage = np.zeros((56,56))
                count += 1
                
    def _extract(self):
        #image = cv2.imread("output4.jpg", cv2.CV_LOAD_IMAGE_GRAYSCALE)
        for a in range(1,82):
            imageString = ("output" + str(a) +  ".jpg")
            image = cv2.imread(imageString)
            image = image[11:51,11:51]
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            binary = cv2.adaptiveThreshold(
                src=gray, maxValue=255,
                adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                thresholdType=cv2.THRESH_BINARY, blockSize=11, C=2)
            #blurred = cv2.medianBlur(binary, ksize=5)
            #gBlur = cv2.GaussianBlur(blurred, (5,5), 0)
            #sharpened = cv2.addWeighted(binary, 1, gBlur, -2.5, 255)
            blurred = cv2.medianBlur(binary, ksize=5)
            gBlur = cv2.GaussianBlur(blurred, (5,5), 0)
            sharpened = cv2.addWeighted(binary, 1, gBlur, -2.55, 255)
            cv2.imwrite("output" + str(a) + ".jpg", sharpened)
        

        
if __name__ == "__main__":
    sudoku = Sudoku("sudoku.jpg")
