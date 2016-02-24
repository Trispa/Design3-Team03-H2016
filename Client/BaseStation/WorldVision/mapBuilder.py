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
        blurMapImage = cv2.GaussianBlur(mapImage, (5, 5), 0)
        for gray in cv2.split(blurMapImage):
            for threshold in xrange(0, 255, 24):
                if threshold == 0:
                    binary = cv2.Canny(gray, 0, 50, apertureSize=5)
                    binary = cv2.dilate(binary, None)
                else:
                    retval, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
                contours, hierarchy = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
                for contour in contours:
                    contour_len = cv2.arcLength(contour, True)
                    contour = cv2.approxPolyDP(contour, 0.02*contour_len, True)
                    if cv2.contourArea(contour) > 300 and cv2.isContourConvex(contour):
                        if len(contour) == 3:
                            myShape = Triangle("Triangle", contour)
                        elif len(contour) == 4:
                            myShape = Square("Square", contour)
                        elif len(contour) == 5:
                            myShape = Shape("Pentagone", contour)
                        elif len(contour) > 5:
                            myShape = Shape("Circle", contour)

                        if myShape.isEqualEdges():
                            if myShape.checkAngleValue():
                                self.__map.addShape(myShape)

        return self.__map
