import cv2
import numpy as np
from shape import Shape
from Robot import Robot
from allShapes import Square
from Client.BaseStation.Logic.Pathfinding.Pathfinder import Pathfinder
from Client.BaseStation.Logic.MapCoordinatesAjuster import MapCoordinatesAjuster
import math
import copy

class Map:

    SAFE_MARGIN = 100

    def __init__(self):
        self.__shapes = []
        self.limit = Square("limit", np.array([[]], dtype=np.int32))
        self.robot = Robot(Shape("robot", np.array([[]], dtype=np.int32)), Shape("orientation", np.array([[]], dtype=np.int32)))
        self.target = None
        self.treasures = []

    def getShapesList(self):
        return self.__shapes

    def getContourList(self):
        contourList = []
        for shape in self.__shapes:
            contourList.append(shape.getContour())
        return contourList

    def getMapLimit(self):
        return self.limit

    def getAverageShapeSize(self):
        averageSize = 0
        if len(self.__shapes) > 0:
            for shape in self.__shapes:
                averageSize += shape.getArea()
            averageSize = averageSize/len(self.__shapes)
        return averageSize

    def getGreenSquare(self):
        return self.greenSquare

    def getPositionInFrontOfTreasure(self):
        myPathFinder = Pathfinder(self)
        orientation = 0
        myMapCoorDinateAjuster = MapCoordinatesAjuster(self)
        for treasurePosition in self.treasures:
            if treasurePosition[1] == self.limit.getMaxCorner()[1]:
                orientation = 90
                inFrontPosition = (treasurePosition[0], treasurePosition[1] - self.SAFE_MARGIN)
            elif treasurePosition[1] == self.limit.getMinCorner()[1]:
                orientation = 270
                inFrontPosition = (treasurePosition[0], treasurePosition[1] + self.SAFE_MARGIN)
            else:
                orientation = 180
                inFrontPosition = (treasurePosition[0] + self.SAFE_MARGIN, treasurePosition[1])


            myPath = myPathFinder.findPath(myMapCoorDinateAjuster.convertPoint((self.robot.center)), myMapCoorDinateAjuster.convertPoint(inFrontPosition))
            if len(myPath) > 1:
                return myPath, orientation
        return False


    def setShapes(self, shapes):
        self.__shapes = shapes

    def setMapLimit(self, contour):
        cornerList = []
        minX = 0
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
            if(corner[1] < minY):
                minY = corner[1]
        newFoundLimit = Square("limit", np.array([[[minX,minY + 5]],[[minX,maxY - 5]],[[maxX, maxY - 5]],[[maxX,minY + 5]]], dtype=np.int32))

        if newFoundLimit.getArea() < self.limit.getArea() or len(self.limit.getContour()) == 0:
            self.limit = newFoundLimit

    def setShapesColor(self, mapImage):
        for shape in self.__shapes:
            shape.setColor(copy.copy(mapImage))

    def setTarget(self, target):
        self.target =  target.getShape(self.__shapes)

    def setTreasures(self, relativeAngles):
        rightAngle = 90
        yDistanceFromPurpleCircle = 15
        cameraDistanceFromBackgroundWall = self.robot.purpleCircle.findCenterOfMass()[0] - 20 - self.limit.getMinCorner()[0]
        cameraDistanceFromLowerWall = self.limit.getMaxCorner()[1] - self.robot.purpleCircle.findCenterOfMass()[1] - yDistanceFromPurpleCircle
        cameraDistanceFromUpperWall = self.robot.purpleCircle.findCenterOfMass()[1] - yDistanceFromPurpleCircle - self.limit.getMinCorner()[1]
        for cameraAngle in relativeAngles:

            lowerWall = True

            if cameraAngle < rightAngle:
                xDistanceOfTreasureFromCamera = math.tan(math.radians(cameraAngle))*cameraDistanceFromLowerWall
                treasurePosition = (cameraDistanceFromBackgroundWall - xDistanceOfTreasureFromCamera, self.limit.getMaxCorner()[1])
            else:
                lowerWall = False
                cameraAngle = 180 - cameraAngle
                xDistanceOfTreasureFromCamera = math.tan(math.radians(cameraAngle))*cameraDistanceFromUpperWall
                treasurePosition = (cameraDistanceFromBackgroundWall - xDistanceOfTreasureFromCamera, self.limit.getMinCorner()[1])

            treasureDistanceFromBackground = cameraDistanceFromBackgroundWall - xDistanceOfTreasureFromCamera
            if treasureDistanceFromBackground < 0:
                yDistanceFromCamera = (-1 * (treasureDistanceFromBackground)) / math.tan(math.radians(cameraAngle))
                if lowerWall:
                    treasurePosition = (self.limit.getMinCorner()[0], self.limit.getMaxCorner()[1] - yDistanceFromCamera)
                else:
                    treasurePosition = (self.limit.getMinCorner()[0], self.limit.getMinCorner()[1] + yDistanceFromCamera)


            self.treasures.append(treasurePosition)

    def findSimilarShape(self, newPossibleshape):

        newContourCenterOfMassX, newContourCenterOfMassY = newPossibleshape.findCenterOfMass()
        for shapeAlreadyFound in self.__shapes:
            oldContourCenterOfMassX, oldContourCenterOfMassY = shapeAlreadyFound.findCenterOfMass()
            if(abs(newContourCenterOfMassX - oldContourCenterOfMassX) < 20 and abs(newContourCenterOfMassY - oldContourCenterOfMassY) < 20):
                return shapeAlreadyFound
        return None

    def addShape(self, shapeToAdd):

        if abs(shapeToAdd.getArea() - self.getAverageShapeSize()) < 1100 or len(self.__shapes) < 3:
            similarShape = self.findSimilarShape(shapeToAdd)
            if similarShape != None:
                if similarShape.getArea() < shapeToAdd.getArea() and similarShape.getName() == shapeToAdd.getName():
                    self.__shapes.remove(similarShape)
                    self.__shapes.append(shapeToAdd)
            if similarShape == None:
                self.__shapes.append(shapeToAdd)

    def deleteBlackShapes(self):
        for shape in self.__shapes:
            if shape.getColorName() == "Black":
                self.__shapes.remove(shape)

    def deleteShape(self, shapeToDelete):
        self.__shapes.remove(shapeToDelete)

    def deleteOutsiderShapes(self):
        shapesToDelete = []
        for shape in self.__shapes:
            if shape.isOutside(self.limit):
                shapesToDelete.append(shape)

        for shape in shapesToDelete:
            self.__shapes.remove(shape)

    def filterRobot(self):
        shapes = self.__shapes
        for shape in shapes:
            if(shape.myColor.colorName == "Black" or shape.myColor.colorName == "Purple"):
                self.__shapes.remove(shape)





