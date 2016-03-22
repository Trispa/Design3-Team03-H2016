import cv2
import map
import numpy as np
from colorContainer import ColorContainer
from Factories.ShapeFactory import ShapeFactory
from Factories.ColorFactory import ColorFactory

class MapBuilder:

    def __init__(self):
        self.__map = map.Map()
        self.shapeFactory = ShapeFactory()

    def filterFoundContours(self, contours):
        for contour in contours:
            contour_len = cv2.arcLength(contour, True)
            contour = cv2.approxPolyDP(contour, 0.02*contour_len, True)
            if cv2.contourArea(contour) > 300 and cv2.isContourConvex(contour):
                myShape = self.shapeFactory.ConstructShape(contour)
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
                    binary = cv2.Canny(gray, 0, 100, apertureSize=5)
                    binary = cv2.dilate(binary, None)
                else:
                    retval, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
                contours, hierarchy = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
                for contour in contours:
                    contour_len = cv2.arcLength(contour, True)
                    lessPreciseContour = cv2.approxPolyDP(contour, 0.05*contour_len, True)
                    contour = cv2.approxPolyDP(contour, 0.02*contour_len, True)

                    if cv2.contourArea(contour) > 900 and cv2.isContourConvex(contour) and cv2.contourArea(contour) < 30000:
                        myShape = self.shapeFactory.ConstructShape(contour)
                        myShape.setColor(mapImage)
                        if(myShape.getColorName() == "Pink"):
                            map.robot.circle = myShape
                        elif(myShape.getColorName() == "Black" and (len(myShape.getContour()) == 4 or len(myShape.getContour()) == 5)):
                            map.robot.square = myShape
                        elif myShape.isEqualEdges() and myShape.checkAngleValue():
                            map.addShape(myShape)

                    if cv2.contourArea(contour) > 300000 and cv2.isContourConvex(contour):
                        if len(contour) == 4:
                            map.setMapLimit(contour)

                    if cv2.contourArea(lessPreciseContour) > 300000 and cv2.isContourConvex(lessPreciseContour):
                        if len(lessPreciseContour) == 4:
                            map.setMapLimit(lessPreciseContour)

        self.buildByColorClosing(mapImage, map)
        self.buildByColorOpening(mapImage, map)
        map.setShapesColor(mapImage)
        map.filterRobot()
        map.deleteBlackShapes()

        return map

    def buildByColorClosing(self, mapImage, map):

        for color in ColorContainer.islandColors:
            hsvImage = cv2.cvtColor(mapImage,cv2.COLOR_BGR2HSV)
            coloredImage = cv2.inRange(hsvImage,color.lower,color.higher)

            kernel = np.ones((5,5),np.uint8)
            closing = cv2.morphologyEx(coloredImage, cv2.MORPH_CLOSE, kernel)

            contours, hierarchy = cv2.findContours(closing, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                cnt_len = cv2.arcLength(contour, True)
                contour = cv2.approxPolyDP(contour, 0.02*cnt_len, True)
                if cv2.isContourConvex(contour) and cv2.contourArea(contour) > 100:
                    myShape = self.shapeFactory.ConstructShape(contour)

                    if myShape.isEqualEdges() and myShape.checkAngleValue():
                        map.addShape(myShape)

        return map

    def buildByColorOpening(self, mapImage, map):

        for color in ColorContainer.islandColors:
            hsvImage = cv2.cvtColor(mapImage,cv2.COLOR_BGR2HSV)
            coloredImage = cv2.inRange(hsvImage,color.lower,color.higher)

            kernel = np.ones((5,5),np.uint8)
            closing = cv2.morphologyEx(coloredImage, cv2.MORPH_OPEN, kernel)

            contours, hierarchy = cv2.findContours(closing, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                cnt_len = cv2.arcLength(contour, True)
                contour = cv2.approxPolyDP(contour, 0.02*cnt_len, True)
                if cv2.isContourConvex(contour) and cv2.contourArea(contour) > 300:
                    myShape = self.shapeFactory.ConstructShape(contour)

                    if myShape.isEqualEdges() and myShape.checkAngleValue():
                        map.addShape(myShape)

        return map