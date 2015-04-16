import Image
import cv2
import numpy as np
import math
from matplotlib import pyplot as plt

class Sudoku:
    
    def __init__(self, imagepath):
        self.image = cv2.imread(imagepath)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self._noiseRemove()

        #self._getBox()
        self._findContour()
        
    def _noiseRemove(self):
        blurred = cv2.GaussianBlur(self.image,(5,5), 0)
        unsharp = self.image - blurred
        self.image = self.image + unsharp
        self.Canny = cv2.Canny(self.image, 100,200, apertureSize = 3)
        
        cv2.imwrite("output.jpg", self.Canny)
        
        
    def _getBox(self):

        lines = cv2.HoughLines(self.Canny,1,np.pi/180,150)
        for rho,theta in lines[0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))

            cv2.line(self.image,(x1,y1),(x2,y2),(0,0,255),2)

        cv2.imwrite('houghlines3.jpg',self.image)
        
    def _findContour(self):
        contours, hierarchy = cv2.findContours(self.Canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        img = cv2.drawContours(self.Canny, contours, -1, (0,255,0), 3)
        cv2.imwrite("contours.jpg", img)


    
if __name__ == '__main__':
    Sudoku("sudoku.jpg")