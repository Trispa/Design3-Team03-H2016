import cv2
import numpy as np
import shape
import copy

class Map:

    def __init__(self):
        self.__shapes = []

    def findSimilarShape(self, newPossibleshape):
        newContourCenterOfMassX, newContourCenterOfMassY = newPossibleshape.findCenterOfMass()
        for shapeAlreadyFound in self.__shapes:
            oldContourCenterOfMassX, oldContourCenterOfMassY = shapeAlreadyFound.findCenterOfMass()
            if(abs(newContourCenterOfMassX - oldContourCenterOfMassX) < 10 and abs(newContourCenterOfMassY - oldContourCenterOfMassY) < 10):
                return shapeAlreadyFound
        return None

    def addShape(self, shapeToAdd):
        similarShape = self.findSimilarShape(shapeToAdd)
        if similarShape != None:
            if similarShape.getArea() < shapeToAdd.getArea():
                self.__shapes.remove(similarShape)
                self.__shapes.append(shapeToAdd)
        if similarShape == None:
            self.__shapes.append(shapeToAdd)

    def getShapesList(self):
        return self.__shapes

    def getContourList(self):
        contourList = []
        for shape in self.__shapes:
            contourList.append(shape.getContour())

        return contourList

    def setShapes(self, shapes):
        self.__shapes = shapes

    def setShapesColor(self, mapImage):
        for shape in self.__shapes:
            shape.setColor(copy.copy(mapImage))



