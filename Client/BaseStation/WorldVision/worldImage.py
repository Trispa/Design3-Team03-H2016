import cv2
import numpy as np
import mapBuilder as MB
import map
import copy
from Client.BaseStation.Logic.Pathfinding.Pathfinder import Pathfinder
from Client.BaseStation.Logic.MapCoordinatesAjuster import MapCoordinatesAjuster

class WorldImage:

    def __init__(self, mapImage):
        self.__myMapBuilder = MB.MapBuilder()
        self.__mapImage = mapImage
        self.__map = map.Map()


    def setImage(self, mapImage):
        self.__mapImage = mapImage

    def setTarget(self, target):
        self.__map.setTarget(target)

    def defineTreasures(self, relativeAngles):
        self.__map.setTreasures(relativeAngles)

    def findBestTresor(self):
        self.myPath, ret = self.__map.getPositionInFrontOfTreasure()

        return self.__map.getPositionInFrontOfTreasure()

    def buildMap(self, mapImage):
        self.__map = self.__myMapBuilder.buildMapWithAllFilter(mapImage, self.__map)

    def updateRobotPosition(self, mapImage):
        self.__myMapBuilder.updateRobotPosition(mapImage, self.__map)

        if len(self.__map.robot.blackCircle.getContour()) > 0:
            robot = [self.__map.robot.blackCircle.getContour()]
        else:
            robot = []

        if len(self.__map.robot.purpleCircle.getContour()) > 0:
            orientation = [self.__map.robot.purpleCircle.getContour()]
        else:
            orientation = []

        cv2.drawContours( mapImage, orientation, -1, (0, 255, 0), 3 )
        cv2.drawContours( mapImage, robot, -1, (0, 255, 0), 3 )

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

        if self.__map.target != None:
            target = [self.__map.target.getContour()]
        else:
            target = []

        for treasure in self.__map.treasures:
            cv2.circle(frame,(int(treasure[0]), int(treasure[1])), 10, (17,148,162), 2)

        # for compteur in range (1, self.myPath.__len__()):
        #     startLine = (self.myPath[compteur-1].positionX,self.myPath[compteur-1].positionY)
        #     endLine =  (self.myPath[compteur].positionX,self.myPath[compteur].positionY)
        #     cv2.line(frame, (int(startLine[0]), int(startLine[1])), (int(endLine[0]), int(endLine[1])),(0, 0, 255), 2, 1)

        cv2.drawContours( frame, self.__map.getContourList(), -1, (0, 255, 0), 3 )
        cv2.drawContours( frame, limit, -1, (0, 255, 0), 3 )
        cv2.drawContours( frame, target, -1, (255, 0, 0), 3 )



        return frame
