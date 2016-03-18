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
        self.endNodeGenerator = EndNodeGenerator(self.MAP_SIZE_X, self.MAP_SIZE_Y, self.SAFE_MARGIN, obstaclesList,
                                                 self.collisionDetector)
        self.obstaclesList = obstaclesList
        self.graph = Graph()
        self.obstaclesList.sort(key=lambda obstacle: obstacle.positionX)


    def generateGraph(self):
        firstObstacle = self.obstaclesList[0]
        self.__defaultStart(firstObstacle)

        for compteur in range(0, self.obstaclesList.__len__()):
            currentObstacle = self.obstaclesList[(compteur)]
            startingNode = currentObstacle.startingNode
            print currentObstacle.positionX, currentObstacle.positionY, "compteur:", compteur
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
            if self.__isCollidingWithWallFront(currentObstacle) == False:
                self.__generateFrontPath(borderNodeLeftBottom, borderNodeLeftTop, currentObstacle, startingNode)

            if self.__isCollidingWithWallUpper(currentObstacle) == False:
                self.__generateTopPath(collisionUpperLeftCorner, collisionUpperRightCorner,
                                   currentObstacle, borderNodeLeftTop, currentOstacleTopLeftCorner, borderNodeRightTop)

            if self.__isCollidingWithWallLower(currentObstacle) == False:
                self.__generateBottomPath(collisionBottomLeftCorner, collisionBottomRightCorner, currentObstacle,
                                     borderNodeLeftBottom, currentOstacleBottomLeftCorner, borderNodeRightBottom)

            if self.__isCollidingWithWallBack(currentObstacle) == False:
                self.__generateEndPath(borderNodeRightBottom, borderNodeRightTop, currentObstacle, endNode)

        return self.graph

    def __generateEndPath(self, borderNodeRightBottom, borderNodeRightTop, currentObstacle, endNode):
        if self.__hasEndInnerCollision(currentObstacle) == False:
            if self.__isCollidingWithWallUpper(currentObstacle) == False:
                self.graph.connectTwoNodes(borderNodeRightTop, endNode)

            if self.__isCollidingWithWallLower(currentObstacle) == False:
                self.graph.connectTwoNodes(borderNodeRightBottom, endNode)
        else:
            result, collidingObstacle = self.__hasLowerInnerCollision(currentObstacle)
            if result == False or collidingObstacle[-1].positionX < currentObstacle.positionX:
                if self.__isCollidingWithWallLower(currentObstacle) == False:
                    self.graph.connectTwoNodes(borderNodeRightBottom, endNode)

            result, collidingObstacle = self.__hasUpperInnerCollision(currentObstacle)
            if result == False or collidingObstacle[-1].positionX < currentObstacle.positionX:
                if self.__isCollidingWithWallUpper(currentObstacle):
                    self.graph.connectTwoNodes(borderNodeRightTop, endNode)

    def __generateFrontPath(self, borderNodeLeftBottom, borderNodeLeftTop, currentObstacle, startingNode):
        if self.__hasFrontalInnerCollision(currentObstacle) == False:
            if self.__isCollidingWithWallLower(currentObstacle) == False:
                self.graph.connectTwoNodes(startingNode, borderNodeLeftBottom)

            if self.__isCollidingWithWallUpper(currentObstacle) == False:
                self.graph.connectTwoNodes(startingNode, borderNodeLeftTop)

        else:
            result, collidingObstacle = self.__hasUpperInnerCollision(currentObstacle)

            if result == False or collidingObstacle[0].positionX > currentObstacle.positionX:
                if self.__isCollidingWithWallUpper(currentObstacle) == False:
                    self.graph.connectTwoNodes(startingNode, borderNodeLeftTop)

            result, collidingObstacle = self.__hasLowerInnerCollision(currentObstacle)
            if result == False or collidingObstacle[0].positionX > currentObstacle.positionX:
                if self.__isCollidingWithWallLower(currentObstacle) == False:
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
        result, collidingObstacle = self.__hasLowerInnerCollision(currentObstacle)
        if collisionBottomLeftCorner.positionY == self.MAP_SIZE_Y and collisionBottomRightCorner.positionY == self.MAP_SIZE_Y:
            self.graph.connectTwoNodes(borderNodeLeftBottom, borderNodeRightBottom)

        elif (
                collisionBottomLeftCorner.positionY != self.MAP_SIZE_Y and collisionBottomRightCorner.positionY == self.MAP_SIZE_Y) or goodRightCollision.positionY >= collisionBottomLeftCorner.positionY or collidingObstacle.__contains__(collisionBottomLeftCorner):
            if result == False:
                print currentObstacle.positionX, currentObstacle.positionY, "botafett"
                tempNode = Node((collisionBottomLeftCorner.positionX + self.SAFE_MARGIN, borderNodeLeftBottom.positionY))
                self.graph.connectTwoNodes(borderNodeLeftBottom, tempNode)

        else:

            safeZoneCornerBotLeft = (bottomLeftCorner[0], collisionBottomLeftCorner.positionY - self.SAFE_MARGIN)
            safeZoneCornerTopRight = (goodRightCollision.positionX - self.SAFE_MARGIN, bottomLeftCorner[1])
            safeZoneCornerTopLeft = (bottomLeftCorner[0], bottomLeftCorner[1])
            tempNode = Node(
                SafeZone(safeZoneCornerTopLeft, safeZoneCornerTopRight, safeZoneCornerBotLeft).getCenterOfSafeZone())
            tempNode.isASafeNode = True
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
        result, collidingObstacle = self.__hasUpperInnerCollision(currentObstacle)
        print goodRightCollision, goodRightCollision.positionX, goodRightCollision.positionY
        print collisionUpperLeftCorner, collisionUpperLeftCorner.positionX, collisionUpperLeftCorner.positionY
        if collisionUpperLeftCorner.positionY == 0 and collisionUpperRightCorner.positionY == 0:
            self.graph.connectTwoNodes(borderNodeLeftTop, borderNodeRightTop)

        elif (
                collisionUpperLeftCorner.positionY != 0 and collisionUpperRightCorner.positionY == 0) or (goodRightCollision.positionY <= collisionUpperLeftCorner.positionY) or (collidingObstacle.__contains__(collisionUpperLeftCorner)):
            if result == False:
                print collidingObstacle.__contains__(collisionUpperLeftCorner)
                print collisionUpperLeftCorner
                tempNode = Node((collisionUpperLeftCorner.positionX + self.SAFE_MARGIN, borderNodeLeftTop.positionY))
                self.graph.connectTwoNodes(borderNodeLeftTop, tempNode)

        else:
            print currentObstacle.positionX, currentObstacle.positionY, "topafett2"
            safeZoneCornerTopLeft = (topLeftCorner[0], collisionUpperLeftCorner.positionY + self.SAFE_MARGIN)
            safeZoneCornerTopRight = (
            goodRightCollision.positionX - self.SAFE_MARGIN, collisionUpperLeftCorner.positionY + self.SAFE_MARGIN)
            safeZoneCornerBotLeft = (topLeftCorner[0], topLeftCorner[1])
            tempNode = Node(
                SafeZone(safeZoneCornerTopLeft, safeZoneCornerTopRight, safeZoneCornerBotLeft).getCenterOfSafeZone())
            tempNode.isASafeNode = True
            goodRightCollision.setStartingNode(tempNode)
            self.graph.connectTwoNodes(borderNodeLeftTop, tempNode)


    def __hasFrontalInnerCollision(self, obstacle):
        for compteur in range(0, self.obstaclesList.__len__()):
            currentObstacle = self.obstaclesList[compteur]
            if currentObstacle != obstacle:
                if currentObstacle.positionY <= obstacle.positionY + 2*self.SAFE_MARGIN and currentObstacle.positionY >= obstacle.positionY - 2*self.SAFE_MARGIN:
                    if currentObstacle.positionX <= obstacle.positionX and currentObstacle.positionX >= obstacle.positionX - 2*self.SAFE_MARGIN:
                        return True
        return False


    def __hasEndInnerCollision(self, obstacle):
        for compteur in range(0, self.obstaclesList.__len__()):
            currentObstacle = self.obstaclesList[compteur]
            if currentObstacle != obstacle:
                if currentObstacle.positionY <= obstacle.positionY + 2*self.SAFE_MARGIN and currentObstacle.positionY >= obstacle.positionY - 2*self.SAFE_MARGIN:
                    if currentObstacle.positionX >= obstacle.positionX and currentObstacle.positionX <= obstacle.positionX + 2*self.SAFE_MARGIN:
                        return True
        return False


    def __hasUpperInnerCollision(self, obstacle):
        obstacleCollision = []
        result = False
        for compteur in range(0, self.obstaclesList.__len__()):
            currentObstacle = self.obstaclesList[compteur]
            if currentObstacle != obstacle:
                if currentObstacle.positionX <= obstacle.positionX + 2*self.SAFE_MARGIN and currentObstacle.positionX >= obstacle.positionX - 2*self.SAFE_MARGIN:
                    if currentObstacle.positionY < obstacle.positionY and currentObstacle.positionY >= obstacle.positionY - 2*self.SAFE_MARGIN:
                        result = True
                        obstacleCollision.append(currentObstacle)
        return result, obstacleCollision


    def __hasLowerInnerCollision(self, obstacle):
        obstacleCollision = []
        result = False
        for compteur in range(0, self.obstaclesList.__len__()):
            currentObstacle = self.obstaclesList[compteur]
            if currentObstacle != obstacle:
                if currentObstacle.positionX <= obstacle.positionX + 2*self.SAFE_MARGIN and currentObstacle.positionX >= obstacle.positionX - 2*self.SAFE_MARGIN:
                    if currentObstacle.positionY > obstacle.positionY and currentObstacle.positionY <= obstacle.positionY + 2*self.SAFE_MARGIN:
                        result = True
                        obstacleCollision.append(currentObstacle)
        return result, obstacleCollision

    def __isCollidingWithWallLower(self, obstacle):
        if obstacle.positionY >= self.MAP_SIZE_Y - 2*self.SAFE_MARGIN:
            return True
        return False

    def __isCollidingWithWallUpper(self, obstacle):
        if obstacle.positionY <= 0 + 2*self.SAFE_MARGIN:
            return True
        return False


    def __isCollidingWithWallFront(self, obstacle):
        if obstacle.positionX <= 0 + 2*self.SAFE_MARGIN:
            return True
        return False


    def __isCollidingWithWallBack(self, obstacle):
        if obstacle.positionX >= self.MAP_SIZE_X - 2*self.SAFE_MARGIN:
            return True
        return False


    def __defaultStart(self, firstObstacle):
        safeZoneCornerTopLeft = (0, 0)
        safeZoneCornerBotLeft = (0, self.MAP_SIZE_Y)
        safeZoneCornerTopRight = (firstObstacle.positionX - self.SAFE_MARGIN, safeZoneCornerTopLeft[1])
        startingNode = Node(
            SafeZone(safeZoneCornerTopLeft, safeZoneCornerTopRight, safeZoneCornerBotLeft).getCenterOfSafeZone())
        startingNode.isASafeNode = True
        firstObstacle.setStartingNode(startingNode)
