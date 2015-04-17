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

    
    def _noiseRemove(self):
        print "True"
        
        gray = cv2.GaussianBlur(self.image,(5,5),0)
        thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)
        cv2.imwrite("thresh.jpg", thresh)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
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
        print "True"
        cv2.drawContours(self.image, [biggest], 0, (0,255,0), 10)
        cv2.imwrite("contours.jpg", self.image)
if __name__ == "__main__":
    sudoku = Sudoku("sudoku.jpg")