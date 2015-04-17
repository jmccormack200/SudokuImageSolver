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
        #self.Canny = cv2.GaussianBlur(self.image,(3,3), 0)
        
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

        large_Contour = 0
        max_area = [0,0,0,0,0,0,0,0,0]
        contour_list = [0,0,0,0,0,0,0,0,0]
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 100:
                perimeter = cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, 0.02*perimeter, True)
                for a in range(len(max_area)-1,-1,-1):
                    #print area
                    #print a
                    print max_area
                    if area > max_area[a] and len(approx)==4:
                        if a > 0:
                            for b in range(0,a):
                                contour_list[b] = contour_list[b+1]
                                max_area[b-1] = max_area[b]
                        contour_list[a] = contour
                        max_area[a] = area
                        break
                    #print max_area
        #print contour_list
        for a in range(len(contour_list)):
            print contour_list[a][0]
            cv2.drawContours(self.image, contour_list, a, (0,255,0), 10)
        cv2.imwrite("contours.jpg", self.image)
        

    
if __name__ == '__main__':
    Sudoku("sudoku.jpg")