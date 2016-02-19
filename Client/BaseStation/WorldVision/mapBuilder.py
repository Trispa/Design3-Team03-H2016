import cv2
import numpy as np
import map
import copy
import shape
import square
from color import Color

class MapBuilder:

    colors = []
    colors.append(Color(np.uint8([[[0,255,0]]]), "Green"))
    colors.append(Color(np.uint8([[[255,0,0]]]), "Blue"))
    colors.append(Color(np.uint8([[[150,179,255]]]), "Red"))
    colors.append(Color(np.uint8([[[0,255,255]]]), "Yellow"))

    def __init__(self):
        self.__map = map.Map()

    def buildByColorClosing(self, mapImage):

        for color in self.colors:
            hsvImage = cv2.cvtColor(mapImage,cv2.COLOR_BGR2HSV)
            coloredImage = cv2.inRange(hsvImage,color.lower,color.higher)

            kernel = np.ones((5,5),np.uint8)
            closing = cv2.morphologyEx(coloredImage, cv2.MORPH_CLOSE, kernel)

            contours, hierarchy = cv2.findContours(closing, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
                if cv2.isContourConvex(cnt) and cv2.contourArea(cnt) > 100:
                    if len(cnt) == 3:
                        myShape = shape.Shape("Triangle", cnt)
                    elif len(cnt) == 4:
                        myShape = square.Square("Square", cnt)
                    elif len(cnt) == 5:
                        myShape = shape.Shape("Pentagone", cnt)
                    elif len(cnt) > 5:
                        myShape = shape.Shape("Circle", cnt)

                    if myShape.isEqualEdges() and myShape.checkAngleValue():
                        self.__map.addShape(myShape)

        return self.__map

    #Trouve le triangle vert
    def buildByColorOpening(self, mapImage):

        for color in self.colors:
            hsvImage = cv2.cvtColor(mapImage,cv2.COLOR_BGR2HSV)
            coloredImage = cv2.inRange(hsvImage,color.lower,color.higher)

            kernel = np.ones((5,5),np.uint8)
            opening = cv2.morphologyEx(coloredImage, cv2.MORPH_OPEN, kernel)

            contours, hierarchy = cv2.findContours(opening, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
                if cv2.isContourConvex(cnt) and cv2.contourArea(cnt) > 100:
                    if len(cnt) == 3:
                        myShape = shape.Shape("Triangle", cnt)
                    elif len(cnt) == 4:
                        myShape = square.Square("Square", cnt)
                    elif len(cnt) == 5:
                        myShape = shape.Shape("Pentagone", cnt)
                    elif len(cnt) > 5:
                        myShape = shape.Shape("Circle", cnt)

                    if myShape.isEqualEdges() and myShape.checkAngleValue():
                        self.__map.addShape(myShape)

        return self.__map

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
                            myShape = shape.Shape("Triangle", cnt)
                        elif len(cnt) == 4:
                            myShape = square.Square("Square", cnt)
                        elif len(cnt) == 5:
                            myShape = shape.Shape("Pentagone", cnt)
                        elif len(cnt) > 5:
                            myShape = shape.Shape("Circle", cnt)

                        if myShape.checkAngleValue() and myShape.isEqualEdges():
                            self.__map.addShape(myShape)

        return self.__map
