import cv2
import numpy as np
import map
import copy
from shape import Shape
from allShapes import Square, Triangle

class MapBuilder:

    def __init__(self):
        self.__map = map.Map()

    def filterFoundContours(self, contours):
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

                if myShape.isEqualEdges() and myShape.checkAngleValue():
                    self.__map.addShape(myShape)

            if cv2.contourArea(contour) > 300000 and cv2.isContourConvex(contour):
                if len(contour) == 4:
                    self.__map.setMapLimit(contour)


    def buildMapWithAllFilter(self, mapImage, map):
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
                    if cv2.contourArea(contour) > 300 and cv2.isContourConvex(contour) and cv2.contourArea(contour) < 300000:
                        if len(contour) == 3:
                            myShape = Triangle("Triangle", contour)
                        elif len(contour) == 4:
                            myShape = Square("Square", contour)
                        elif len(contour) == 5:
                            myShape = Shape("Pentagone", contour)
                        elif len(contour) > 5:
                            myShape = Shape("Circle", contour)

                        if myShape.isEqualEdges() and myShape.checkAngleValue():
                            map.addShape(myShape)

                    if cv2.contourArea(contour) > 300000 and cv2.isContourConvex(contour):
                        if len(contour) == 4:
                            map.setMapLimit(contour)

        if (len(map.getMapLimit().getContour()[0]) == 4):
            map.deleteOutsiderShapes()
        map.setShapesColor(mapImage)
        return map

    def buildByColorClosing(self, mapImage):

        for color in self.colors:
            hsvImage = cv2.cvtColor(mapImage,cv2.COLOR_BGR2HSV)
            coloredImage = cv2.inRange(hsvImage,color.lower,color.higher)

            kernel = np.ones((5,5),np.uint8)
            closing = cv2.morphologyEx(coloredImage, cv2.MORPH_CLOSE, kernel)

            contours, hierarchy = cv2.findContours(closing, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            self.filterFoundContours(contours)

        return self.__map
