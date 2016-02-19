import cv2
import numpy as np
import shape

class Map:

    def __init__(self, shapes = []):
        self.__shapes = shapes



    def findSimilarShape(self, shape):
        newContourCenterOfMassX, newContourCenterOfMassY = shape.findCenterOfMass()
        for shapeAlreadyFound in self.__shapes:
            oldContourCenterOfMassX, oldContourCenterOfMassY = shapeAlreadyFound.findCenterOfMass()
            if(abs(newContourCenterOfMassX - oldContourCenterOfMassX) < 10 and abs(newContourCenterOfMassY - oldContourCenterOfMassY) < 10):
                return shapeAlreadyFound
        return None

    #TODO
    def addShape(self, shapeToAdd):
        similarShape = self.findSimilarShape(shapeToAdd)
        #if similarShape != None:
         #   if similarShape.getArea < shapeToAdd.getArea:
          #      self.__shapes.remove(similarShape)
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

    def mergeShapeList(self, otherMap):
        shapesDifference = []

        for otherMapShape in otherMap.getShapesList():
            notInShapeList = True
            for myShape in self.__shapes:
                if otherMapShape.asSimilarCenterOfMass(myShape):
                    notInShapeList = False
            if notInShapeList:
                shapesDifference.append(otherMapShape)

        newMap = Map(shapesDifference)
        return newMap


