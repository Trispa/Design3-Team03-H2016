from Client.BaseStation.Logic.Pathfinding.Graph.Node import Node
from Client.BaseStation.Logic.Pathfinding.Graph.SafeZone import SafeZone


class EndNodeGenerator:
    def __init__(self, mapSizeX, mapSizeY, safeMargin, obstacleList, collisionDetector, graph):
        self.MAP_SIZE_X = mapSizeX
        self.MAP_SIZE_Y = mapSizeY
        self.SAFE_MARGIN = safeMargin
        self.collisionDetector = collisionDetector
        self.obstaclesList = obstacleList
        self.graph = graph

    def generateEndNode(self, currentObstacle, topRightCorner, bottomRightCorner, collisionBottomRightCorner, collisionUpperRightCorner, compteur):
        if (collisionBottomRightCorner.positionY != self.MAP_SIZE_Y and collisionUpperRightCorner.positionY != 0):
            endNode = self.__twoCollision(collisionBottomRightCorner, collisionUpperRightCorner, topRightCorner,
                                          bottomRightCorner, currentObstacle)

        elif (collisionBottomRightCorner.positionY != self.MAP_SIZE_Y ^ collisionUpperRightCorner.positionY != 0):
            endNode = self.__onlyOneCollision(bottomRightCorner, collisionBottomRightCorner, collisionUpperRightCorner,
                                              topRightCorner)

        elif (collisionBottomRightCorner.positionY == self.MAP_SIZE_Y and collisionUpperRightCorner.positionY == 0):
                endNode = self.__noCollision(compteur, currentObstacle)

        return endNode


    def __noCollision(self, compteur, currentObstacle):
        if self.collisionDetector.isCollidingWithWallBack(currentObstacle) == False:
            safeZoneCornerTopLeft = (currentObstacle.positionX + self.SAFE_MARGIN, 0)
            safeZoneCornerBotLeft = (currentObstacle.positionX + self.SAFE_MARGIN, self.MAP_SIZE_Y)
            if (compteur == self.obstaclesList.__len__() - 1):
                safeZoneCornerTopRight = (self.MAP_SIZE_X, 0)
                safeZone = SafeZone(safeZoneCornerTopLeft, safeZoneCornerTopRight, safeZoneCornerBotLeft)
                endNode = safeZone.getCenterNodeOfSafeZone()
                self.graph.safeZonesList.append(safeZone)
            else:
                safeZoneCornerTopRight = (self.obstaclesList[compteur + 1].positionX - self.SAFE_MARGIN, 0)
                safeZone = SafeZone(safeZoneCornerTopLeft, safeZoneCornerTopRight, safeZoneCornerBotLeft)
                endNode = safeZone.getCenterNodeOfSafeZone()
                self.graph.safeZonesList.append(safeZone)
                self.obstaclesList[compteur+1].setStartingNode(endNode)
            endNode.isASafeNode = True
            return endNode


    def __twoCollision(self, collisionBottomRightCorner, collisionUpperRightCorner, topRightCorner, bottomRightCorner, currentObstacle):
        safeZoneCornerTopLeft = (topRightCorner[0], collisionUpperRightCorner.positionY + self.SAFE_MARGIN)
        safeZoneCornerBotLeft = (bottomRightCorner[0], collisionBottomRightCorner.positionY - self.SAFE_MARGIN)

        if (collisionBottomRightCorner.positionX < collisionUpperRightCorner.positionX) and collisionBottomRightCorner.positionX != currentObstacle.positionX:
            collisionUpperLeftCornerTemp, collisionUpperRightCornerTemp, collisionBottomLeftCornerTemP, collisionBottomRightCornerTemp = self.collisionDetector.detectStackedObstacleXAxis(
                collisionBottomRightCorner)

            if collisionUpperRightCornerTemp != collisionUpperRightCorner:
                safeZoneCornerTopRight = (collisionUpperRightCornerTemp.positionX - self.SAFE_MARGIN,
                            collisionUpperRightCorner.positionY + self.SAFE_MARGIN)
                safeZone = SafeZone(safeZoneCornerTopLeft, safeZoneCornerTopRight, safeZoneCornerBotLeft)
                endNode = safeZone.getCenterNodeOfSafeZone()
                self.graph.safeZonesList.append(safeZone)
                collisionUpperRightCornerTemp.setStartingNode(endNode)
                endNode.isASafeNode = True

            else:
                endNode = (Node((collisionBottomRightCorner.positionX + self.SAFE_MARGIN,
                                 (collisionBottomRightCorner.positionY + collisionUpperRightCorner.positionY) / 2)))
                safeZoneCornerBotLeft = (bottomRightCorner[0], collisionBottomRightCorner.positionY - self.SAFE_MARGIN)
                safeZoneCornerTopRight = (collisionBottomRightCorner.positionX + self.SAFE_MARGIN, collisionUpperRightCorner.positionY + self.SAFE_MARGIN)
                safeZoneCornerTopLeft = (bottomRightCorner[0], collisionUpperRightCorner.positionY + self.SAFE_MARGIN)
                tempNode = self.graph.generateSafeZone(safeZoneCornerBotLeft, safeZoneCornerTopLeft, safeZoneCornerTopRight)
                self.graph.connectTwoNodes(endNode, tempNode)

        else:
            collisionUpperLeftCornerTemp, collisionUpperRightCornerTemp, collisionBottomLeftCornerTemp, collisionBottomRightCornerTemp = self.collisionDetector.detectStackedObstacleXAxis(
                collisionUpperRightCorner)

            if collisionBottomRightCornerTemp != collisionBottomRightCorner:
                safeZoneCornerTopRight = (collisionBottomRightCornerTemp.positionX - self.SAFE_MARGIN,
                            collisionUpperRightCorner.positionY + self.SAFE_MARGIN)
                safeZone = SafeZone(safeZoneCornerTopLeft, safeZoneCornerTopRight, safeZoneCornerBotLeft)
                endNode = safeZone.getCenterNodeOfSafeZone()
                self.graph.safeZonesList.append(safeZone)
                collisionBottomRightCornerTemp.setStartingNode(endNode)
                endNode.isASafeNode = True

            else:
                endNode = (Node((collisionUpperRightCorner.positionX + self.SAFE_MARGIN,
                                 (collisionBottomRightCorner.positionY + collisionUpperRightCorner.positionY) / 2)))
                safeZoneCornerBotLeft = (bottomRightCorner[0], collisionBottomRightCorner.positionY - self.SAFE_MARGIN)
                safeZoneCornerTopRight = (collisionUpperRightCorner.positionX + self.SAFE_MARGIN, collisionBottomRightCorner.positionY + self.SAFE_MARGIN)
                safeZoneCornerTopLeft = (bottomRightCorner[0], collisionUpperRightCorner.positionY + self.SAFE_MARGIN)
                tempNode = self.graph.generateSafeZone(safeZoneCornerBotLeft, safeZoneCornerTopLeft, safeZoneCornerTopRight)
                self.graph.connectTwoNodes(endNode, tempNode)
        return endNode


    def __onlyOneCollision(self, bottomRightCorner, collisionBottomRightCorner, collisionUpperRightCorner,
                           topRightCorner):
        safeZoneCornerTopLeft = (topRightCorner[0], collisionUpperRightCorner.positionY + self.SAFE_MARGIN)
        safeZoneCornerBotLeft = (bottomRightCorner[0], collisionBottomRightCorner.positionY - self.SAFE_MARGIN)
        if collisionBottomRightCorner.positionY != self.MAP_SIZE_Y:
            collisionUpperLeftCornerTemp, collisionUpperRightCornerTemp, collisionBottomLeftCornerTemP, collisionBottomRightCornerTemp = self.collisionDetector.detectStackedObstacleXAxis(
                collisionBottomRightCorner)

            if collisionUpperRightCornerTemp.positionY != 0:
                safeZoneCornerTopRight = (collisionUpperRightCornerTemp.positionX - self.SAFE_MARGIN,
                            collisionUpperRightCorner.positionY + self.SAFE_MARGIN)
                safeZone = SafeZone(safeZoneCornerTopLeft, safeZoneCornerTopRight, safeZoneCornerBotLeft)
                endNode = safeZone.getCenterNodeOfSafeZone()
                self.graph.safeZonesList.append(safeZone)
                collisionUpperRightCornerTemp.setStartingNode(endNode)
                endNode.isASafeNode = True

            else:
                endNode = (Node((collisionBottomRightCorner.positionX + self.SAFE_MARGIN,
                                 (collisionBottomRightCorner.positionY + collisionUpperRightCorner.positionY) / 2)))
                safeZoneCornerBotLeft = (bottomRightCorner[0], collisionBottomRightCorner.positionY - self.SAFE_MARGIN)
                safeZoneCornerTopRight = (collisionBottomRightCorner.positionX + self.SAFE_MARGIN, 0 + self.SAFE_MARGIN)
                safeZoneCornerTopLeft = (bottomRightCorner[0], 0 + self.SAFE_MARGIN)
                tempNode = self.graph.generateSafeZone(safeZoneCornerBotLeft, safeZoneCornerTopLeft, safeZoneCornerTopRight)
                self.graph.connectTwoNodes(endNode, tempNode)

        else:
            collisionUpperLeftCornerTemp, collisionUpperRightCornerTemp, collisionBottomLeftCornerTemp, collisionBottomRightCornerTemp = self.collisionDetector.detectStackedObstacleXAxis(
                collisionUpperRightCorner)

            if collisionBottomRightCornerTemp.positionY != self.MAP_SIZE_Y:
                safeZoneCornerTopRight = (collisionBottomRightCornerTemp.positionX - self.SAFE_MARGIN,
                            collisionUpperRightCorner.positionY + self.SAFE_MARGIN)
                safeZone = SafeZone(safeZoneCornerTopLeft, safeZoneCornerTopRight, safeZoneCornerBotLeft)
                endNode = safeZone.getCenterNodeOfSafeZone()
                self.graph.safeZonesList.append(safeZone)
                endNode.isASafeNode = True
                collisionBottomRightCornerTemp.setStartingNode(endNode)

            else:
                endNode = (Node((collisionUpperRightCorner.positionX + self.SAFE_MARGIN,
                                 (collisionBottomRightCorner.positionY + collisionUpperRightCorner.positionY) / 2)))
                safeZoneCornerBotLeft = (bottomRightCorner[0], self.MAP_SIZE_Y - self.SAFE_MARGIN)
                safeZoneCornerTopRight = (collisionUpperRightCorner.positionX + self.SAFE_MARGIN, collisionUpperRightCorner.positionY + self.SAFE_MARGIN)
                safeZoneCornerTopLeft = (bottomRightCorner[0], collisionUpperRightCorner.positionY + self.SAFE_MARGIN)
                tempNode = self.graph.generateSafeZone(safeZoneCornerBotLeft, safeZoneCornerTopLeft, safeZoneCornerTopRight)
                self.graph.connectTwoNodes(endNode, tempNode)
        return endNode

