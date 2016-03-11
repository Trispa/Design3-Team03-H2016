import cv2
import numpy as np

from Client.BaseStation.Logic.Pathfinding.Graph.CollisionDetector import CollisionDetector
from Client.BaseStation.Logic.Pathfinding.Graph.EndNodeGenerator import EndNodeGenerator
from Client.BaseStation.Logic.Pathfinding.Graph.Node import Node
from Client.BaseStation.Logic.Pathfinding.Graph.SafeZone import SafeZone
from Client.BaseStation.Logic.Pathfinding.Graph.Graph import Graph


class GraphGenerator:
    SAFE_MARGIN = 30

    def __init__(self, obstaclesList, mapSizeX, mapSizeY):
        self.MAP_SIZE_X = mapSizeX
        self.MAP_SIZE_Y = mapSizeY
        self.collisionDetector = CollisionDetector(self.MAP_SIZE_X, self.MAP_SIZE_Y, self.SAFE_MARGIN, obstaclesList)
        self.endNodeGenerator = EndNodeGenerator(self.MAP_SIZE_X, self.MAP_SIZE_Y, self.SAFE_MARGIN, obstaclesList, self.collisionDetector)
        self.obstaclesList = obstaclesList
        self.graph = Graph()
        self.obstaclesList.sort(key=lambda obstacle: obstacle.positionX)


    def generateGraph(self):
        firstObstacle = self.obstaclesList[0]
        if (firstObstacle.positionX - self.SAFE_MARGIN > 0):
            self.__defaultStart(firstObstacle)

            compteur = 0

        else:
            #quand colle au mur en partant TO DO
            pass
            compteur = 1

        for compteur in range (compteur, self.obstaclesList.__len__()):
            currentObstacle = self.obstaclesList[(compteur)]
            print "obstacle:", currentObstacle.positionX, currentObstacle.positionY, currentObstacle
            startingNode = currentObstacle.startingNode
            if compteur < self.obstaclesList.__len__()-1:
                nextObstacle = self.obstaclesList[compteur+1]
                if nextObstacle.startingNode.positionX == 0:

                    nextObstacle.setStartingNode(currentObstacle.startingNode)


            topLeftCorner = (currentObstacle.positionX - self.SAFE_MARGIN, currentObstacle.positionY - self.SAFE_MARGIN)
            topRightCorner = (currentObstacle.positionX + self.SAFE_MARGIN, currentObstacle.positionY - self.SAFE_MARGIN)
            bottomRightCorner = (currentObstacle.positionX + self.SAFE_MARGIN, currentObstacle.positionY + self.SAFE_MARGIN)
            bottomLeftCorner = (currentObstacle.positionX - self.SAFE_MARGIN, currentObstacle.positionY + self.SAFE_MARGIN)
            collisionUpperLeftCorner, collisionUpperRightCorner, collisionBottomLeftCorner, collisionBottomRightCorner = self.collisionDetector.detectStackedObstacleXAxis(currentObstacle)

            borderNodeLeftTop = Node(
            (topLeftCorner[0], (topLeftCorner[1] + collisionUpperLeftCorner.positionY + self.SAFE_MARGIN) / 2))
            self.graph.connectTwoNodes(startingNode, borderNodeLeftTop)

            borderNodeRightTop = Node(
            (topRightCorner[0], (topRightCorner[1] + collisionUpperRightCorner.positionY + self.SAFE_MARGIN) / 2))
            self.__generateTopPath(collisionUpperLeftCorner, collisionUpperRightCorner,
                                   currentObstacle, borderNodeLeftTop, topLeftCorner, borderNodeRightTop)
                
            borderNodeLeftBottom = Node((bottomLeftCorner[0], (bottomLeftCorner[1]+collisionBottomLeftCorner.positionY-self.SAFE_MARGIN)/2))
            self.graph.connectTwoNodes(startingNode,borderNodeLeftBottom)
            
            borderNodeRightBottom = Node((bottomRightCorner[0], (bottomRightCorner[1]+collisionBottomRightCorner.positionY-self.SAFE_MARGIN)/2))
            self.__generateBottomPath(collisionBottomLeftCorner, collisionBottomRightCorner, currentObstacle, borderNodeLeftBottom, bottomLeftCorner, borderNodeRightBottom)

            endNode = self.endNodeGenerator.generateEndNode(currentObstacle, topRightCorner, bottomRightCorner, collisionBottomRightCorner, collisionUpperRightCorner, compteur)
            self.graph.connectTwoNodes(borderNodeRightTop,endNode)
            self.graph.connectTwoNodes(borderNodeRightBottom,endNode)
        return self.graph


    def __generateBottomPath(self, collisionBottomLeftCorner, collisionBottomRightCorner, currentObstacle, borderNodeLeftBottom,
                             bottomLeftCorner, borderNodeRightBottom):
        goodRightCollision = collisionBottomRightCorner
        collisionUpperLeftCornerTemp, collisionUpperRightCornerTemp, collisionBottomLeftCornerTemp, collisionBottomRightCornerTemp = self.collisionDetector.detectStackedObstacleXAxis(
                    goodRightCollision)
        while (collisionUpperLeftCornerTemp == currentObstacle and collisionBottomLeftCornerTemp.positionY != self.MAP_SIZE_Y and collisionBottomLeftCornerTemp.positionX > currentObstacle.positionX):

            goodRightCollision = collisionBottomLeftCornerTemp

            collisionUpperLeftCornerTemp, collisionUpperRightCornerTemp, collisionBottomLeftCornerTemp, collisionBottomRightCornerTemp = self.collisionDetector.detectStackedObstacleXAxis(
                    goodRightCollision)

        if collisionBottomLeftCorner.positionY == self.MAP_SIZE_Y and collisionBottomRightCorner.positionY == self.MAP_SIZE_Y:
            self.graph.connectTwoNodes(borderNodeLeftBottom, borderNodeRightBottom)

        elif (collisionBottomLeftCorner.positionY != self.MAP_SIZE_Y and collisionBottomRightCorner.positionY == self.MAP_SIZE_Y) or goodRightCollision.positionY >= collisionBottomLeftCorner.positionY:
            tempNode = Node((collisionBottomLeftCorner.positionX+self.SAFE_MARGIN, borderNodeLeftBottom.positionY))
            self.graph.connectTwoNodes(borderNodeLeftBottom, tempNode)

        else:

            safeZoneCornerBotLeft = (bottomLeftCorner[0], collisionBottomLeftCorner.positionY - self.SAFE_MARGIN)
            safeZoneCornerTopRight = (goodRightCollision.positionX - self.SAFE_MARGIN, bottomLeftCorner[1])
            safeZoneCornerTopLeft = (bottomLeftCorner[0], bottomLeftCorner[1])
            tempNode = Node(SafeZone(safeZoneCornerTopLeft, safeZoneCornerTopRight, safeZoneCornerBotLeft).getCenterOfSafeZone())
            goodRightCollision.setStartingNode(tempNode)
            self.graph.connectTwoNodes(borderNodeLeftBottom, tempNode)




    def __generateTopPath(self, collisionUpperLeftCorner, collisionUpperRightCorner, currentObstacle, borderNodeLeftTop,
                          topLeftCorner, borderNodeRightTop):
        goodRightCollision = collisionUpperRightCorner
        collisionUpperLeftCornerTemp, collisionUpperRightCornerTemp, collisionBottomLeftCornerTemp, collisionBottomRightCornerTemp = self.collisionDetector.detectStackedObstacleXAxis(
                    goodRightCollision)
        while (collisionBottomLeftCornerTemp == currentObstacle and collisionUpperLeftCornerTemp.positionY != 0 and collisionUpperLeftCornerTemp.positionX > currentObstacle.positionX):

            goodRightCollision = collisionUpperLeftCornerTemp

            collisionUpperLeftCornerTemp, collisionUpperRightCornerTemp, collisionBottomLeftCornerTemp, collisionBottomRightCornerTemp = self.collisionDetector.detectStackedObstacleXAxis(
                    goodRightCollision)

        if collisionUpperLeftCorner.positionY == 0 and collisionUpperRightCorner.positionY == 0:
            self.graph.connectTwoNodes(borderNodeLeftTop, borderNodeRightTop)

        elif (collisionUpperLeftCorner.positionY != 0 and collisionUpperRightCorner.positionY == 0) or goodRightCollision.positionY <= collisionUpperLeftCorner.positionY:
            tempNode = Node((collisionUpperLeftCorner.positionX+self.SAFE_MARGIN, borderNodeLeftTop.positionY))
            self.graph.connectTwoNodes(borderNodeLeftTop, tempNode)

        else:
            safeZoneCornerTopLeft = (topLeftCorner[0], collisionUpperLeftCorner.positionY + self.SAFE_MARGIN)
            safeZoneCornerTopRight = (goodRightCollision.positionX - self.SAFE_MARGIN, collisionUpperLeftCorner.positionY + self.SAFE_MARGIN)
            safeZoneCornerBotLeft = (topLeftCorner[0], topLeftCorner[1])
            tempNode = Node(SafeZone(safeZoneCornerTopLeft, safeZoneCornerTopRight, safeZoneCornerBotLeft).getCenterOfSafeZone())
            goodRightCollision.setStartingNode(tempNode)
            self.graph.connectTwoNodes(borderNodeLeftTop, tempNode)


    def __defaultStart(self, firstObstacle):
        safeZoneCornerTopLeft = (0, 0)
        safeZoneCornerBotLeft = (0, self.MAP_SIZE_Y)
        safeZoneCornerTopRight = (firstObstacle.positionX - self.SAFE_MARGIN, safeZoneCornerTopLeft[1])
        startingNode = Node(SafeZone(safeZoneCornerTopLeft, safeZoneCornerTopRight, safeZoneCornerBotLeft).getCenterOfSafeZone())
        firstObstacle.setStartingNode(startingNode)


    



