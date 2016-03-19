import cv2
import numpy as np

from Client.BaseStation.Logic.Pathfinding.Graph.CollisionDetector import CollisionDetector
from Client.BaseStation.Logic.Pathfinding.Graph.EndNodeGenerator import EndNodeGenerator
from Client.BaseStation.Logic.Pathfinding.Graph.Node import Node
from Client.BaseStation.Logic.Pathfinding.Graph.SafeZone import SafeZone
from Client.BaseStation.Logic.Pathfinding.Graph.Graph import Graph



class GraphGenerator:
    SAFE_MARGIN = 60

    def __init__(self, obstaclesList, mapSizeX, mapSizeY):
        self.MAP_SIZE_X = mapSizeX
        self.MAP_SIZE_Y = mapSizeY
        self.graph = Graph(obstaclesList, self.SAFE_MARGIN)
        self.collisionDetector = CollisionDetector(self.MAP_SIZE_X, self.MAP_SIZE_Y, self.SAFE_MARGIN, obstaclesList)
        self.endNodeGenerator = EndNodeGenerator(self.MAP_SIZE_X, self.MAP_SIZE_Y, self.SAFE_MARGIN, obstaclesList,
                                                 self.collisionDetector, self.graph)
        self.obstaclesList = obstaclesList

        self.obstaclesList.sort(key=lambda obstacle: obstacle.positionX)


    def generateGraph(self):
        firstObstacle = self.obstaclesList[0]
        if self.collisionDetector.isCollidingWithWallFront(firstObstacle) == False:
            self.__defaultStart(firstObstacle)

        for compteur in range(0, self.obstaclesList.__len__()):
            currentObstacle = self.obstaclesList[(compteur)]
            startingNode = currentObstacle.startingNode
            if compteur < self.obstaclesList.__len__() - 1:
                nextObstacle = self.obstaclesList[compteur + 1]
                if nextObstacle.startingNode.positionX == 0:
                    nextObstacle.setStartingNode(currentObstacle.startingNode)

            currentOstacleTopLeftCorner = (currentObstacle.positionX - self.SAFE_MARGIN, currentObstacle.positionY - self.SAFE_MARGIN)
            currentOstacleTopRightCorner = (currentObstacle.positionX + self.SAFE_MARGIN, currentObstacle.positionY - self.SAFE_MARGIN)
            currentOstacleBottomRightCorner = (currentObstacle.positionX + self.SAFE_MARGIN, currentObstacle.positionY + self.SAFE_MARGIN)
            currentOstacleBottomLeftCorner = (currentObstacle.positionX - self.SAFE_MARGIN, currentObstacle.positionY + self.SAFE_MARGIN)

            collisionUpperLeftCorner, collisionUpperRightCorner, collisionBottomLeftCorner, collisionBottomRightCorner = self.collisionDetector.detectStackedObstacleXAxis(currentObstacle)

            borderNodeLeftTop = Node(
                (currentOstacleTopLeftCorner[0], (currentOstacleTopLeftCorner[1] + collisionUpperLeftCorner.positionY + self.SAFE_MARGIN) / 2))
            borderNodeRightTop = Node(
                (currentOstacleTopRightCorner[0], (currentOstacleTopRightCorner[1] + collisionUpperRightCorner.positionY + self.SAFE_MARGIN) / 2))
            borderNodeLeftBottom = Node((currentOstacleBottomLeftCorner[0],
                (currentOstacleBottomLeftCorner[1] + collisionBottomLeftCorner.positionY - self.SAFE_MARGIN) / 2))
            borderNodeRightBottom = Node((currentOstacleBottomRightCorner[0],
                (currentOstacleBottomRightCorner[1] + collisionBottomRightCorner.positionY - self.SAFE_MARGIN) / 2))
            endNode = self.endNodeGenerator.generateEndNode(currentObstacle, currentOstacleTopRightCorner, currentOstacleBottomRightCorner,
                                                            collisionBottomRightCorner, collisionUpperRightCorner, compteur)
            if self.collisionDetector.isCollidingWithWallFront(currentObstacle) == False:
                self.__generateFrontPath(borderNodeLeftBottom, borderNodeLeftTop, currentObstacle, startingNode)

            if self.collisionDetector.isCollidingWithWallUpper(currentObstacle) == False:
                self.__generateTopPath(collisionUpperLeftCorner, collisionUpperRightCorner,
                                   currentObstacle, borderNodeLeftTop, currentOstacleTopLeftCorner, borderNodeRightTop)

            if self.collisionDetector.isCollidingWithWallLower(currentObstacle) == False:
                self.__generateBottomPath(collisionBottomLeftCorner, collisionBottomRightCorner, currentObstacle,
                                     borderNodeLeftBottom, currentOstacleBottomLeftCorner, borderNodeRightBottom)

            if self.collisionDetector.isCollidingWithWallBack(currentObstacle) == False:
                self.__generateEndPath(borderNodeRightBottom, borderNodeRightTop, currentObstacle, endNode)

        return self.graph


    def __generateEndPath(self, borderNodeRightBottom, borderNodeRightTop, currentObstacle, endNode):
        if self.collisionDetector.hasEndInnerCollision(currentObstacle) == False:
            if self.collisionDetector.isCollidingWithWallUpper(currentObstacle) == False:
                self.graph.connectTwoNodes(borderNodeRightTop, endNode)

            if self.collisionDetector.isCollidingWithWallLower(currentObstacle) == False:
                self.graph.connectTwoNodes(borderNodeRightBottom, endNode)
        else:
            result, collidingObstacle = self.collisionDetector.hasLowerInnerCollision(currentObstacle)
            if result == False or collidingObstacle[-1].positionX < currentObstacle.positionX:
                if self.collisionDetector.isCollidingWithWallLower(currentObstacle) == False:
                    self.graph.connectTwoNodes(borderNodeRightBottom, endNode)

            result, collidingObstacle = self.collisionDetector.hasUpperInnerCollision(currentObstacle)
            if result == False or collidingObstacle[-1].positionX < currentObstacle.positionX:
                if self.collisionDetector.isCollidingWithWallUpper(currentObstacle) == False:
                    self.graph.connectTwoNodes(borderNodeRightTop, endNode)


    def __generateFrontPath(self, borderNodeLeftBottom, borderNodeLeftTop, currentObstacle, startingNode):
        if self.collisionDetector.hasFrontalInnerCollision(currentObstacle) == False:
            if self.collisionDetector.isCollidingWithWallLower(currentObstacle) == False:
                self.graph.connectTwoNodes(startingNode, borderNodeLeftBottom)

            if self.collisionDetector.isCollidingWithWallUpper(currentObstacle) == False:
                self.graph.connectTwoNodes(startingNode, borderNodeLeftTop)

        else:
            result, collidingObstacle = self.collisionDetector.hasUpperInnerCollision(currentObstacle)

            if result == False or collidingObstacle[0].positionX > currentObstacle.positionX:
                if self.collisionDetector.isCollidingWithWallUpper(currentObstacle) == False:
                    self.graph.connectTwoNodes(startingNode, borderNodeLeftTop)

            result, collidingObstacle = self.collisionDetector.hasLowerInnerCollision(currentObstacle)
            if result == False or collidingObstacle[0].positionX > currentObstacle.positionX:
                if self.collisionDetector.isCollidingWithWallLower(currentObstacle) == False:
                    self.graph.connectTwoNodes(startingNode, borderNodeLeftBottom)


    def __generateBottomPath(self, collisionBottomLeftCorner, collisionBottomRightCorner, currentObstacle,
                             borderNodeLeftBottom,
                             bottomLeftCorner, borderNodeRightBottom):
        goodRightCollision = collisionBottomRightCorner
        collisionUpperLeftCornerTemp, collisionUpperRightCornerTemp, collisionBottomLeftCornerTemp, collisionBottomRightCornerTemp = self.collisionDetector.detectStackedObstacleXAxis(
            goodRightCollision)
        while (
                    collisionUpperLeftCornerTemp == currentObstacle and collisionBottomLeftCornerTemp.positionY != self.MAP_SIZE_Y and collisionBottomLeftCornerTemp.positionX > currentObstacle.positionX):
            goodRightCollision = collisionBottomLeftCornerTemp

            collisionUpperLeftCornerTemp, collisionUpperRightCornerTemp, collisionBottomLeftCornerTemp, collisionBottomRightCornerTemp = self.collisionDetector.detectStackedObstacleXAxis(
                goodRightCollision)
        result, collidingObstacle = self.collisionDetector.hasLowerInnerCollision(currentObstacle)
        if collisionBottomLeftCorner.positionY == self.MAP_SIZE_Y and collisionBottomRightCorner.positionY == self.MAP_SIZE_Y:
            safeZoneCornerBotLeft = (bottomLeftCorner[0], collisionBottomLeftCorner.positionY - self.SAFE_MARGIN)
            safeZoneCornerTopRight = (borderNodeRightBottom.positionX, bottomLeftCorner[1])
            safeZoneCornerTopLeft = (bottomLeftCorner[0], bottomLeftCorner[1])
            tempNode = self.graph.generateSafeZone(safeZoneCornerBotLeft, safeZoneCornerTopLeft, safeZoneCornerTopRight)
            self.graph.connectTwoNodes(borderNodeLeftBottom, tempNode)
            self.graph.connectTwoNodes(borderNodeRightBottom, tempNode)

        elif (
                collisionBottomLeftCorner.positionY != self.MAP_SIZE_Y and collisionBottomRightCorner.positionY == self.MAP_SIZE_Y) or goodRightCollision.positionY >= collisionBottomLeftCorner.positionY or collidingObstacle.__contains__(collisionBottomLeftCorner):
            if result == False:
                tempNode = Node((collisionBottomLeftCorner.positionX + self.SAFE_MARGIN, borderNodeLeftBottom.positionY))

                safeZoneCornerBotLeft = (borderNodeLeftBottom[0], collisionBottomLeftCorner.positionY - self.SAFE_MARGIN)
                safeZoneCornerTopRight = (tempNode.positionX, bottomLeftCorner[1])
                safeZoneCornerTopLeft = (bottomLeftCorner[0], bottomLeftCorner[1])
                safeNode = self.graph.generateSafeZone(safeZoneCornerBotLeft, safeZoneCornerTopLeft, safeZoneCornerTopRight)

                self.graph.connectTwoNodes(borderNodeLeftBottom, safeNode)
                self.graph.connectTwoNodes(safeNode, tempNode)

        else:

            safeZoneCornerBotLeft = (bottomLeftCorner[0], collisionBottomLeftCorner.positionY - self.SAFE_MARGIN)
            safeZoneCornerTopRight = (goodRightCollision.positionX - self.SAFE_MARGIN, bottomLeftCorner[1])
            safeZoneCornerTopLeft = (bottomLeftCorner[0], bottomLeftCorner[1])
            tempNode = self.graph.generateSafeZone(safeZoneCornerBotLeft, safeZoneCornerTopLeft, safeZoneCornerTopRight)
            goodRightCollision.setStartingNode(tempNode)
            self.graph.connectTwoNodes(borderNodeLeftBottom, tempNode)


    def __generateTopPath(self, collisionUpperLeftCorner, collisionUpperRightCorner, currentObstacle, borderNodeLeftTop,
                          topLeftCorner, borderNodeRightTop):
        goodRightCollision = collisionUpperRightCorner
        collisionUpperLeftCornerTemp, collisionUpperRightCornerTemp, collisionBottomLeftCornerTemp, collisionBottomRightCornerTemp = self.collisionDetector.detectStackedObstacleXAxis(
            goodRightCollision)
        while (
                    collisionBottomLeftCornerTemp == currentObstacle and collisionUpperLeftCornerTemp.positionY != 0 and collisionUpperLeftCornerTemp.positionX > currentObstacle.positionX):
            goodRightCollision = collisionUpperLeftCornerTemp

            collisionUpperLeftCornerTemp, collisionUpperRightCornerTemp, collisionBottomLeftCornerTemp, collisionBottomRightCornerTemp = self.collisionDetector.detectStackedObstacleXAxis(
                goodRightCollision)
        result, collidingObstacle = self.collisionDetector.hasUpperInnerCollision(currentObstacle)
        if collisionUpperLeftCorner.positionY == 0 and collisionUpperRightCorner.positionY == 0:
            safeZoneCornerTopLeft = (topLeftCorner[0], collisionUpperLeftCorner.positionY + self.SAFE_MARGIN)
            safeZoneCornerTopRight = (borderNodeRightTop.positionX, collisionUpperLeftCorner.positionY + self.SAFE_MARGIN)
            safeZoneCornerBotLeft = (topLeftCorner[0], topLeftCorner[1])
            tempNode = self.graph.generateSafeZone(safeZoneCornerBotLeft, safeZoneCornerTopLeft, safeZoneCornerTopRight)
            self.graph.connectTwoNodes(borderNodeLeftTop, tempNode)
            self.graph.connectTwoNodes(borderNodeRightTop, tempNode)

        elif (
                collisionUpperLeftCorner.positionY != 0 and collisionUpperRightCorner.positionY == 0) or (goodRightCollision.positionY <= collisionUpperLeftCorner.positionY) or (collidingObstacle.__contains__(collisionUpperLeftCorner)):
            if result == False:
                tempNode = Node((collisionUpperLeftCorner.positionX + self.SAFE_MARGIN, borderNodeLeftTop.positionY))

                safeZoneCornerBotLeft = (borderNodeLeftTop[0], topLeftCorner[1])
                safeZoneCornerTopRight = (tempNode.positionX, collisionUpperLeftCorner.positionY + self.SAFE_MARGIN)
                safeZoneCornerTopLeft = (borderNodeLeftTop[0], collisionUpperLeftCorner.positionY + self.SAFE_MARGIN)
                safeNode = self.graph.generateSafeZone(safeZoneCornerBotLeft, safeZoneCornerTopLeft, safeZoneCornerTopRight)

                self.graph.connectTwoNodes(borderNodeLeftTop, safeNode)
                self.graph.connectTwoNodes(safeNode, tempNode)

        else:
            safeZoneCornerTopLeft = (topLeftCorner[0], collisionUpperLeftCorner.positionY + self.SAFE_MARGIN)
            safeZoneCornerTopRight = (
            goodRightCollision.positionX - self.SAFE_MARGIN, collisionUpperLeftCorner.positionY + self.SAFE_MARGIN)
            safeZoneCornerBotLeft = (topLeftCorner[0], topLeftCorner[1])
            tempNode = self.graph.generateSafeZone(safeZoneCornerBotLeft, safeZoneCornerTopLeft, safeZoneCornerTopRight)
            goodRightCollision.setStartingNode(tempNode)
            self.graph.connectTwoNodes(borderNodeLeftTop, tempNode)

   

    def __defaultStart(self, firstObstacle):
        safeZoneCornerTopLeft = (0, 0)
        safeZoneCornerBotLeft = (0, self.MAP_SIZE_Y)
        safeZoneCornerTopRight = (firstObstacle.positionX - self.SAFE_MARGIN, safeZoneCornerTopLeft[1])
        startingNode = self.graph.generateSafeZone(safeZoneCornerBotLeft, safeZoneCornerTopLeft, safeZoneCornerTopRight)
        firstObstacle.setStartingNode(startingNode)
