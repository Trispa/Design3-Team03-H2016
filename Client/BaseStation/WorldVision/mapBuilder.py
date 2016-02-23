import cv2
import numpy as np
import map
import copy
from shape import Shape
from allShapes import Square, Triangle

from color import Color

class MapBuilder:

    def __init__(self):
        self.__map = map.Map()

    def buildMapWithAllFilter(self, mapImage):
        imgCopy = copy.copy(mapImage)
        img = cv2.GaussianBlur(mapImage, (5, 5), 0)

        for gray in cv2.split(img):
            for thrs in xrange(0, 255, 26):
                if thrs == 0:
                    bin = cv2.Canny(gray, 0, 50, apertureSize=5)
                    bin = cv2.dilate(bin, None)
                else:
                    retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
                contours, hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
                for cnt in contours:
                    cnt_len = cv2.arcLength(cnt, True)
                    cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
                    if cv2.contourArea(cnt) > 300 and cv2.isContourConvex(cnt):
                        if len(cnt) == 3:
                            myShape = Shape("Triangle", cnt)
                        elif len(cnt) == 4:
                            myShape = Square("Square", cnt)
                        elif len(cnt) == 5:
                            myShape = Shape("Pentagone", cnt)
                        elif len(cnt) > 5:
                            myShape = Shape("Circle", cnt)

                        if myShape.checkAngleValue() and myShape.isEqualEdges():
                            self.__map.addShape(myShape)

        return self.__map
