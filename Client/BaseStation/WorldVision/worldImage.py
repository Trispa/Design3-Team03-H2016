import cv2
import numpy as np
import mapBuilder as MB
import map

class WorldImage:

    def __init__(self, mapImage):
        self.__myMapBuilder = MB.MapBuilder()
        self.__mapImage = mapImage
        self.__map = map.Map()


    def setImage(self, mapImage):
        self.__mapImage = mapImage

    def setMap(self):
        self.__map = self.__myMapBuilder.buildMapWithAllFilter(self.__mapImage)

    def defineShapesColor(self):
        self.__map.setShapesColor(self.__mapImage)

    def getMap(self):
        return self.__map

    def addLabels(self):
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.4
        thickness = 1
        mapShapes = self.__map.getShapesList()
        for shape in mapShapes:
            size, baseline = cv2.getTextSize(shape.getName(), font, scale, thickness)
            textWidth = size[0]
            textHeight = size[1]
            x,y,w,h = shape.getBoundingRectangle()
            #Center text
            point = (x + ((w - textWidth) / 2), y + ((h + textHeight) / 2))
            cv2.putText(self.__mapImage, shape.getName(), point, font, scale, (0,0,0), thickness, 8)

    def drawMapOnImage(self):
        cv2.drawContours( self.__mapImage, self.__map.getContourList(), -1, (0, 255, 0), 3 )
        return self.__mapImage
