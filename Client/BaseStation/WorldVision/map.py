import cv2
import numpy as np
from shape import Shape
from Robot import Robot
from allShapes import Square
from Client.BaseStation.Logic.Pathfinding.Pathfinder import Pathfinder
from Client.BaseStation.Logic.Pathfinding.Path import Path
from Client.BaseStation.Logic.MapCoordinatesAjuster import MapCoordinatesAjuster
import math
import copy

class Map:

    SAFE_MARGIN = 130
    SAFE_MARGIN_FOR_TREASURE = 100

    def __init__(self):
        self.__shapes = []
        self.limit = Square("limit", np.array([[]], dtype=np.int32))
        self.robot = Robot(Shape("robot", np.array([[]], dtype=np.int32)), Shape("orientation", np.array([[]], dtype=np.int32)))
        self.target = None
        self.treasures = []
        self.orientationForTreasure = 0

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

    def getEdgeGradiant(self, edge):
        if float(edge[1].item(0) - edge[0].item(0)) != 0 and float(edge[1].item(1) - edge[0].item(1)) != 0:
            edgePerpendicularGradient = float(-1 / (float(float(edge[1].item(1) - edge[0].item(1)) / float(edge[1].item(0) - edge[0].item(0)))))
        elif float(edge[1].item(0) - edge[0].item(0)) == 0:
            edgePerpendicularGradient = float(-1 / (float(float(edge[1].item(1) - edge[0].item(1)) / 0.0001)))
        else:
            edgePerpendicularGradient = float(-1 / 0.00001 / float(edge[1].item(0) - edge[0].item(0)))

        return edgePerpendicularGradient

    def getPositionInFrontOfTreasure(self):
        myPathFinder = Pathfinder(self)
        myMapCoorDinateAjuster = MapCoordinatesAjuster(self)
        myBestPath = Path()
        myBestPath.totalDistance = 99999
        bestInFrontPosition = (0,0)
        bestOrientationForTreasure = 0
        for treasurePosition in self.treasures:
            if not isinstance(myPathFinder.findPath(myMapCoorDinateAjuster.convertPoint((self.robot.center)), myMapCoorDinateAjuster.convertPoint(treasurePosition)), bool):
                if treasurePosition[1] == self.limit.getMaxCorner()[1]:
                    newOrientationForTreasure = 90
                    newInFrontPosition = (treasurePosition[0], treasurePosition[1] - self.SAFE_MARGIN_FOR_TREASURE)
                elif treasurePosition[1] == self.limit.getMinCorner()[1]:
                    newOrientationForTreasure  = 270
                    newInFrontPosition = (treasurePosition[0], treasurePosition[1] + self.SAFE_MARGIN_FOR_TREASURE)
                else:
                    newOrientationForTreasure  = 180
                    newInFrontPosition = (treasurePosition[0] + self.SAFE_MARGIN_FOR_TREASURE, treasurePosition[1])
                    print newInFrontPosition

                myNewPath = myPathFinder.findPath(myMapCoorDinateAjuster.convertPoint((self.robot.center)), myMapCoorDinateAjuster.convertPoint(newInFrontPosition))
                if myNewPath != False:
                    if myNewPath.totalDistance < myBestPath.totalDistance:
                        myBestPath = myNewPath
                        bestOrientationForTreasure = newOrientationForTreasure
                        bestInFrontPosition = newInFrontPosition
        return bestInFrontPosition,bestOrientationForTreasure

    def getPositionInFrontOfIsland(self):
        myPathFinder = Pathfinder(self)
        myPath = Path()
        myPath.totalDistance = 9999
        myMapCoorDinateAjuster = MapCoordinatesAjuster(self)
        myBestPosition = (0,0)
        orientation = 0
        targetShape = self.target
        edgesList = self.target.getEdgesList()
        for edge in edgesList:
            xCenterOfEdge = edge[0].item(0) + (((edge[0].item(0) - edge[1].item(0)) / 2) * -1)
            yCenterOfEdge = edge[0].item(1) + (((edge[0].item(1) - edge[1].item(1)) / 2) * -1)

            edgePerpendicularGradient = self.getEdgeGradiant(edge)

            conversionGradient = 1
            if abs(edgePerpendicularGradient) > 1:
                conversionGradient = 0.1
            if abs(edgePerpendicularGradient) > 10:
                conversionGradient = 0.01
            if self.target.isOutside((xCenterOfEdge + 1 * conversionGradient, yCenterOfEdge + 1 * edgePerpendicularGradient * conversionGradient)):
                positionToGo = (xCenterOfEdge + self.SAFE_MARGIN * conversionGradient, yCenterOfEdge + self.SAFE_MARGIN * edgePerpendicularGradient * conversionGradient)
                hypothenuse = 0
                while hypothenuse < self.SAFE_MARGIN:
                    positionToGo = (positionToGo[0] + 1, positionToGo[1] + edgePerpendicularGradient)
                    opp = abs(yCenterOfEdge - positionToGo[1])
                    adj = abs(xCenterOfEdge - positionToGo[0])
                    hypothenuse = math.sqrt((opp * opp) + (adj * adj))
            else:
                positionToGo = (xCenterOfEdge - self.SAFE_MARGIN * conversionGradient, yCenterOfEdge - self.SAFE_MARGIN * edgePerpendicularGradient * conversionGradient)
                opp = abs(yCenterOfEdge - positionToGo[1])
                adj = abs(xCenterOfEdge - positionToGo[0])
                hypothenuse = math.sqrt((opp * opp) + (adj * adj))
                while hypothenuse < self.SAFE_MARGIN:
                    positionToGo = (positionToGo[0] - 1* conversionGradient, positionToGo[1] - edgePerpendicularGradient* conversionGradient)
                    opp = abs(yCenterOfEdge - positionToGo[1])
                    adj = abs(xCenterOfEdge - positionToGo[0])
                    hypothenuse = math.sqrt((opp * opp) + (adj * adj))

            angle = math.degrees(math.atan2(opp,adj))
            if positionToGo[0] > xCenterOfEdge and positionToGo[1] < yCenterOfEdge:
                angle = 180 - angle
            if positionToGo[0] > xCenterOfEdge and positionToGo[1] > yCenterOfEdge:
                angle = angle + 180
            if positionToGo[0] < xCenterOfEdge and positionToGo[1] > yCenterOfEdge:
                angle = 360 - angle

            myNewPath = myPathFinder.findPath(myMapCoorDinateAjuster.convertPoint((self.robot.center)), myMapCoorDinateAjuster.convertPoint(positionToGo))

            if myNewPath != False:
                if myNewPath.totalDistance < myPath.totalDistance:
                    myPath = myNewPath
                    myBestPosition = positionToGo
                    orientation = angle

        if myBestPosition == (0, 0):
            x,y,width,height = cv2.boundingRect(targetShape.getContour())
            centerOfMassX, centerOfMassY = targetShape.findCenterOfMass()
            point = ((centerOfMassX - (self.SAFE_MARGIN + width), centerOfMassY))
            if myPathFinder.findPath(myMapCoorDinateAjuster.convertPoint((self.robot.center)), myMapCoorDinateAjuster.convertPoint((centerOfMassX - (self.SAFE_MARGIN + width), centerOfMassY))).totalDistance < 99999:
                myBestPosition = (centerOfMassX - (self.SAFE_MARGIN + width), centerOfMassY)
                orientation = 0
            elif myPathFinder.findPath(myMapCoorDinateAjuster.convertPoint((self.robot.center)), myMapCoorDinateAjuster.convertPoint((centerOfMassX + (self.SAFE_MARGIN + width), centerOfMassY))).totalDistance < 99999:
                myBestPosition = (centerOfMassX + (self.SAFE_MARGIN + width), centerOfMassY)
                orientation = 180
            elif myPathFinder.findPath(myMapCoorDinateAjuster.convertPoint((self.robot.center)), myMapCoorDinateAjuster.convertPoint((centerOfMassX, centerOfMassY - (self.SAFE_MARGIN + height)))).totalDistance < 99999:
                myBestPosition = (centerOfMassX, centerOfMassY - (self.SAFE_MARGIN + height))
                orientation = 90
            elif myPathFinder.findPath(myMapCoorDinateAjuster.convertPoint((self.robot.center)), myMapCoorDinateAjuster.convertPoint((centerOfMassX, centerOfMassY + (self.SAFE_MARGIN + height)))).totalDistance < 99999:
                myBestPosition = (centerOfMassX, centerOfMassY + (self.SAFE_MARGIN + height))
                orientation = 270

        print "MEILLEUR ",myBestPosition, ", Orientation :", orientation
        return myBestPosition, orientation



    def setMapLimit(self, contour):
        cornerList = []
        minX = 0
        maxX = 960
        minY = 109
        maxY = 597

        newFoundLimit = Square("limit", np.array([[[minX,minY + 5]],[[minX,maxY - 5]],[[maxX, maxY - 5]],[[maxX,minY + 5]]], dtype=np.int32))

        if newFoundLimit.getArea() < self.limit.getArea() or len(self.limit.getContour()) == 0:
            self.limit = newFoundLimit

    def setShapesColor(self, frame):
        for shape in self.__shapes:
            shape.findColor(copy.copy(frame))

    def setTarget(self, target):
        self.target =  target.getObstacle(self.__shapes)
        print "Target = ", self.target.getName()

    def setTreasures(self, relativeAngles):
        rightAngle = 90
        yDistanceFromPurpleCircle = 25
        cameraDistanceFromBackgroundWall = self.robot.purpleCircle.findCenterOfMass()[0] - 20 - self.limit.getMinCorner()[0]
        cameraDistanceFromLowerWall = self.limit.getMaxCorner()[1] - self.robot.purpleCircle.findCenterOfMass()[1]
        cameraDistanceFromUpperWall = self.robot.purpleCircle.findCenterOfMass()[1] + 105 - self.limit.getMinCorner()[1]
        for cameraAngle in relativeAngles:

            lowerWall = True
            angleError = abs(180 - self.robot.orientation)
            angleError = 0
            if cameraAngle < rightAngle:
                xDistanceOfTreasureFromCamera = math.tan(math.radians(cameraAngle - angleError))*cameraDistanceFromLowerWall
                treasurePosition = (cameraDistanceFromBackgroundWall - xDistanceOfTreasureFromCamera, self.limit.getMaxCorner()[1])
            else:
                lowerWall = False
                cameraAngle = 180 - cameraAngle
                xDistanceOfTreasureFromCamera = math.tan(math.radians(cameraAngle - angleError))*cameraDistanceFromUpperWall
                treasurePosition = (cameraDistanceFromBackgroundWall - xDistanceOfTreasureFromCamera, self.limit.getMinCorner()[1])

            treasureDistanceFromBackground = cameraDistanceFromBackgroundWall - xDistanceOfTreasureFromCamera
            if treasureDistanceFromBackground < 0:
                yDistanceFromCamera = (-1 * (treasureDistanceFromBackground)) / math.tan(math.radians(cameraAngle))
                if lowerWall:
                    treasurePosition = (self.limit.getMinCorner()[0], self.limit.getMaxCorner()[1] - yDistanceFromCamera)
                else:
                    treasurePosition = (self.limit.getMinCorner()[0], self.limit.getMinCorner()[1] + yDistanceFromCamera)

            print "Tresor ajoute ", treasurePosition
            self.treasures.append(treasurePosition)

    def findSimilarShape(self, newPossibleShape):

        newContourCenterOfMassX, newContourCenterOfMassY = newPossibleShape.findCenterOfMass()
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

    def deleteOutsiderShapes(self):
        shapesToDelete = []
        for shape in self.__shapes:
            if shape.isOutsideLimit(self.limit):
                shapesToDelete.append(shape)

        for shape in shapesToDelete:
            self.__shapes.remove(shape)

    def filterRobot(self):
        shapes = self.__shapes
        for shape in shapes:
            if(shape.color.colorName == "Black" or shape.color.colorName == "Purple"):
                self.__shapes.remove(shape)





