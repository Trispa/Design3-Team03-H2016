import cv2
import map
from Factories.ShapeFactory import ShapeFactory

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
                    binary = cv2.Canny(gray, 0, 50, apertureSize=5)
                    binary = cv2.dilate(binary, None)
                else:
                    retval, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
                contours, hierarchy = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
                for contour in contours:
                    contour_len = cv2.arcLength(contour, True)
                    contour = cv2.approxPolyDP(contour, 0.0175*contour_len, True)
                    if cv2.contourArea(contour) > 300 and cv2.isContourConvex(contour) and cv2.contourArea(contour) < 30000:
                        myShape = self.shapeFactory.ConstructShape(contour)
                        if myShape.isEqualEdges() and myShape.checkAngleValue():
                            map.addShape(myShape)

                    if cv2.contourArea(contour) > 300000 and cv2.isContourConvex(contour):
                        if len(contour) == 4:
                            map.setMapLimit(contour)

        map.setShapesColor(mapImage)
        map.filterRobot()
        map.deleteBlackShapes()
        return map
