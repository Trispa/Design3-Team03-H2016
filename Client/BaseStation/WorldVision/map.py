import cv2
import numpy as np
from shape import Shape
from allShapes import Square
import copy

class Map:

    def __init__(self):
        self.__shapes = []
        self.greenSquare = Square("greenSquare", np.array([[]], dtype=np.int32))
        self.limit = Square("limit", np.array([[]], dtype=np.int32))

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

    def getMapLimit(self):
        return self.limit

    def setShapes(self, shapes):
        self.__shapes = shapes

    def setMapLimit(self, contour):
        cornerList = []
        minX = 1000
        maxX = 0
        minY = 1000
        maxY = 0
        for corner in contour:
            cornerList.append((corner.item(0), corner.item(1)))
        for corner in cornerList:
            if(corner[0] > maxX):
                maxX = corner[0]
            if(corner[1] > maxY):
                maxY = corner[1]
            if(corner[0] < minX):
                minX = corner[0]
            if(corner[1] < minY):
                minY = corner[1]
        self.limit = Square("limit", np.array([[[minX,minY + 5],[minX,maxY - 5],[maxX, maxY - 5],[maxX,minY + 5]]], dtype=np.int32))

    def setShapesColor(self, mapImage):
        for shape in self.__shapes:
            shape.setColor(copy.copy(mapImage))

    def getGreenSquare(self):
        return self.greenSquare

    def setGreenSquare(self):
        biggestShape = Shape("Small shape", np.array([[[1,1],[1,2],[2, 2]]], dtype=np.int32))
        for shape in self.__shapes:
            if shape.getArea() > biggestShape.getArea():
                biggestShape = shape

        if biggestShape.getCornerCount() == 4:
            cornerList = []
            minX = 1000
            maxX = 0
            minY = 1000
            maxY = 0
            for corner in biggestShape.getContour()[0]:
                cornerList.append((corner.item(0), corner.item(1)))
            for corner in cornerList:
                if(corner[0] > maxX):
                    maxX = corner[0]
                if(corner[1] > maxY):
                    maxY = corner[1]
                if(corner[0] < minX):
                    minX = corner[0]
                if(corner[1] < minY):
                    minY = corner[1]
            self.greenSquare = Square("greenSquare", np.array([[[minX,minY],[minX,maxY],[maxX, maxY],[maxX,minY]]], dtype=np.int32))
            self.__shapes.remove(biggestShape)

    #TODO
    def deleteOutsiderShapes(self):

        shapesToDelete = []
        for shape in self.__shapes:
            if shape.isOutside(self.limit):
                shapesToDelete.append(shape)

        for shape in shapesToDelete:
            self.__shapes.remove(shape)


    #TODO
    def refactorWithKnowValue(self):
        pass


