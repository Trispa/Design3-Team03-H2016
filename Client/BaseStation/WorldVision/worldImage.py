import cv2
import numpy as np
import mapBuilder as MB
import map
import copy

class WorldImage:

    def __init__(self, mapImage):
        self.__myMapBuilder = MB.MapBuilder()
        self.__mapImage = mapImage
        self.__map = map.Map()


    def setImage(self, mapImage):
        self.__mapImage = mapImage

    def setMap(self, mapImage):
        self.__map = self.__myMapBuilder.buildMapWithAllFilter(mapImage, self.__map)


    def defineShapesColor(self):
        self.__map.setShapesColor(self.__mapImage)

    def getMap(self):
        return self.__map

    def addLabels(self, frame):
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.4
        thickness = 1
        mapShapes = self.__map.getShapesList()
        for shape in mapShapes:
            size, baseline = cv2.getTextSize(shape.getName() + " " + shape.myColor.colorName, font, scale, thickness)
            textWidth = size[0]
            textHeight = size[1]
            x,y,w,h = shape.getBoundingRectangle()
            point = (x + ((w - textWidth) / 2), y + ((h + textHeight) / 2))
            cv2.putText(frame, shape.getName()+ " " + shape.myColor.colorName, point, font, scale, (255,255,255), thickness, 8)

    def drawMapOnImage(self, frame):
        if len(self.__map.getMapLimit().getContour()) > 0:
            limit = [self.__map.getMapLimit().getContour()]
        else:
            limit = []

        if len(self.__map.robot.square.getContour()) > 0:
            robot = [self.__map.robot.square.getContour()]
        else:
            robot = []

        contourList = self.__map.getContourList()
        cv2.drawContours( frame, self.__map.getContourList(), -1, (0, 255, 0), 3 )
        cv2.drawContours( frame, limit, -1, (0, 255, 0), 3 )
        cv2.drawContours( frame, robot, -1, (0, 255, 0), 3 )

        return frame
