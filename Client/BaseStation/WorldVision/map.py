import cv2
import numpy as np
import shape

class Map:

    def __init__(self):
        self.__shapes = []

    def isNotAlreadyFound(self, shape):
        newContourCenterOfMassX, newContourCenterOfMassY = shape.findCenterOfMass()
        for shapeAlreadyFound in self.__shapes:
            oldContourCenterOfMassX, oldContourCenterOfMassY = shapeAlreadyFound.findCenterOfMass()
            if(abs(newContourCenterOfMassX - oldContourCenterOfMassX) < 5 and abs(newContourCenterOfMassY - oldContourCenterOfMassY) < 5):
                return False
        return True

    def addShape(self, shapeToAdd):
        self.__shapes.append(shapeToAdd)

    def getShapesList(self):
        return self.__shapes

    def getContourList(self):
        contourList = []
        for shape in self.__shapes:
            contourList.append(shape.getContour())

        return contourList


