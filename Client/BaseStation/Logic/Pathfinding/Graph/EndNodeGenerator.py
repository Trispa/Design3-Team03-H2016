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


    def generateEndNode(self, currentObstacle, topRightCorner, bottomRightCorner, collisionBottomRightCorner, collisionUpperRightCorner, counter):
        if (collisionBottomRightCorner.positionY != self.MAP_SIZE_Y and collisionUpperRightCorner.positionY != 0):
            endNode = self.__twoCollisionOnTheRightSide(collisionBottomRightCorner, collisionUpperRightCorner, topRightCorner, bottomRightCorner, currentObstacle)

        elif (collisionBottomRightCorner.positionY != self.MAP_SIZE_Y ^ collisionUpperRightCorner.positionY != 0):
            endNode = self.__onlyOneCollision(bottomRightCorner, collisionBottomRightCorner, collisionUpperRightCorner,topRightCorner)

        elif (collisionBottomRightCorner.positionY == self.MAP_SIZE_Y and collisionUpperRightCorner.positionY == 0):
                endNode = self.__noCollisionOnTheRightSide(counter, currentObstacle)

        return endNode


    def __noCollisionOnTheRightSide(self, counter, currentObstacle):
        safeZoneCornerTopLeft = (currentObstacle.positionX + self.SAFE_MARGIN, 0 + (self.SAFE_MARGIN - 20))
        safeZoneCornerBotLeft = (currentObstacle.positionX + self.SAFE_MARGIN, self.MAP_SIZE_Y - (self.SAFE_MARGIN - 20))
        if (counter == self.obstaclesList.__len__() - 1):
            endNode = self.__noCollision_obstacleIsTheLastOne(safeZoneCornerBotLeft, safeZoneCornerTopLeft)
        else:
            endNode = self.__noCollision_ObstacleIsNotTheLastOne(counter, safeZoneCornerBotLeft, safeZoneCornerTopLeft)
        endNode.isASafeNode = True
        return endNode

    def __noCollision_ObstacleIsNotTheLastOne(self, compteur, safeZoneCornerBotLeft, safeZoneCornerTopLeft):
        safeZoneCornerTopRight = (self.obstaclesList[compteur + 1].positionX - self.SAFE_MARGIN, 0 + (self.SAFE_MARGIN - 20))
        safeZone = SafeZone(safeZoneCornerTopLeft, safeZoneCornerTopRight, safeZoneCornerBotLeft)
        endNode = safeZone.getCenterNodeOfSafeZone()
        self.graph.safeZonesList.append(safeZone)
        self.obstaclesList[compteur + 1].setStartingNode(endNode)
        return endNode

    def __noCollision_obstacleIsTheLastOne(self, safeZoneCornerBotLeft, safeZoneCornerTopLeft):
        safeZoneCornerTopRight = (self.MAP_SIZE_X, 0 + (self.SAFE_MARGIN - 20))
        safeZone = SafeZone(safeZoneCornerTopLeft, safeZoneCornerTopRight, safeZoneCornerBotLeft)
        endNode = safeZone.getCenterNodeOfSafeZone()
        self.graph.safeZonesList.append(safeZone)
        return endNode


    def __twoCollisionOnTheRightSide(self, collisionBottomRightCorner, collisionUpperRightCorner, topRightCorner, bottomRightCorner, currentObstacle):
        safeZoneCornerTopLeft = (topRightCorner[0], collisionUpperRightCorner.positionY + self.SAFE_MARGIN)
        safeZoneCornerBotLeft = (bottomRightCorner[0], collisionBottomRightCorner.positionY - self.SAFE_MARGIN)

        if (collisionBottomRightCorner.positionX < collisionUpperRightCorner.positionX) and collisionBottomRightCorner.positionX != currentObstacle.positionX:
            endNode = self.__twoCollision_CollisionBottomIsCloser(bottomRightCorner, collisionBottomRightCorner,
                                                                  collisionUpperRightCorner, safeZoneCornerBotLeft,
                                                                  safeZoneCornerTopLeft)
        else:
            endNode = self.__twoCollision_TopIsCloser(bottomRightCorner, collisionBottomRightCorner,
                                                      collisionUpperRightCorner, safeZoneCornerBotLeft,
                                                      safeZoneCornerTopLeft)
        return endNode


    def __twoCollision_TopIsCloser(self, bottomRightCorner, collisionBottomRightCorner, collisionUpperRightCorner,
                                   safeZoneCornerBotLeft, safeZoneCornerTopLeft):
        collisionUpperLeftCornerTemp, collisionUpperRightCornerTemp, collisionBottomLeftCornerTemp, collisionBottomRightCornerTemp = self.collisionDetector.detectCloserObstacleForEachCornerXAxis(
            collisionUpperRightCorner)
        if collisionBottomRightCornerTemp != collisionBottomRightCorner:
            endNode = self.__ObstacleBetweenTheTwoCollision(
                collisionUpperRightCorner, collisionBottomRightCornerTemp, safeZoneCornerBotLeft,
                safeZoneCornerTopLeft)
        else:
            endNode = self.__twoCollisionTop_NoObstacleBetweenCollisions(bottomRightCorner, collisionBottomRightCorner,
                                                         collisionUpperRightCorner)
        return endNode


    def __twoCollision_CollisionBottomIsCloser(self, bottomRightCorner, collisionBottomRightCorner,
                                               collisionUpperRightCorner, safeZoneCornerBotLeft, safeZoneCornerTopLeft):
        collisionUpperLeftCornerTemp, collisionUpperRightCornerTemp, collisionBottomLeftCornerTemP, collisionBottomRightCornerTemp = self.collisionDetector.detectCloserObstacleForEachCornerXAxis(
            collisionBottomRightCorner)
        if collisionUpperRightCornerTemp != collisionUpperRightCorner:
            endNode = self.__ObstacleBetweenTheTwoCollision(
                collisionUpperRightCorner, collisionUpperRightCornerTemp, safeZoneCornerBotLeft, safeZoneCornerTopLeft)
        else:
            endNode = self.__noObstacleBetweenCollisions(bottomRightCorner, collisionBottomRightCorner,
                                                         collisionUpperRightCorner)
        return endNode


    def __twoCollisionTop_NoObstacleBetweenCollisions(self, bottomRightCorner, collisionBottomRightCorner, collisionUpperRightCorner):
        endNode = (Node((collisionUpperRightCorner.positionX + self.SAFE_MARGIN,
                         (collisionBottomRightCorner.positionY + collisionUpperRightCorner.positionY) / 2)))
        safeZoneCornerBotLeft = (bottomRightCorner[0], collisionBottomRightCorner.positionY - self.SAFE_MARGIN)
        safeZoneCornerTopRight = (collisionUpperRightCorner.positionX + self.SAFE_MARGIN,
                                  collisionUpperRightCorner.positionY + self.SAFE_MARGIN)
        safeZoneCornerTopLeft = (bottomRightCorner[0], collisionUpperRightCorner.positionY+self.SAFE_MARGIN)
        tempNode = self.graph.generateSafeZone(safeZoneCornerBotLeft, safeZoneCornerTopLeft, safeZoneCornerTopRight)
        self.graph.connectTwoNodes(endNode, tempNode)
        return endNode


    def __noObstacleBetweenCollisions(self, bottomRightCorner, collisionBottomRightCorner, collisionUpperRightCorner):
        endNode = (Node((collisionBottomRightCorner.positionX + self.SAFE_MARGIN,
                         (collisionBottomRightCorner.positionY + collisionUpperRightCorner.positionY) / 2)))
        safeZoneCornerBotLeft = (bottomRightCorner[0], collisionBottomRightCorner.positionY - self.SAFE_MARGIN)
        safeZoneCornerTopRight = (collisionBottomRightCorner.positionX + self.SAFE_MARGIN,
                                  collisionUpperRightCorner.positionY + self.SAFE_MARGIN)
        safeZoneCornerTopLeft = (bottomRightCorner[0], collisionUpperRightCorner.positionY + self.SAFE_MARGIN)
        tempNode = self.graph.generateSafeZone(safeZoneCornerBotLeft, safeZoneCornerTopLeft, safeZoneCornerTopRight)
        self.graph.connectTwoNodes(endNode, tempNode)
        return endNode


    def __onlyOneCollision(self, bottomRightCorner, collisionBottomRightCorner, collisionUpperRightCorner,
                           topRightCorner):
        safeZoneCornerTopLeft = (topRightCorner[0], collisionUpperRightCorner.positionY + self.SAFE_MARGIN)
        safeZoneCornerBotLeft = (bottomRightCorner[0], collisionBottomRightCorner.positionY - self.SAFE_MARGIN)
        if collisionBottomRightCorner.positionY != self.MAP_SIZE_Y:
            endNode = self.__oneCollision_CollisionIsBottom(bottomRightCorner, collisionBottomRightCorner,
                                                            collisionUpperRightCorner, safeZoneCornerBotLeft,
                                                            safeZoneCornerTopLeft)
        else:
            endNode = self.__oneCollision_CollisionIsTop(bottomRightCorner, collisionBottomRightCorner,
                                                         collisionUpperRightCorner, safeZoneCornerBotLeft,
                                                         safeZoneCornerTopLeft)
        return endNode


    def __oneCollision_CollisionIsTop(self, bottomRightCorner, collisionBottomRightCorner, collisionUpperRightCorner,
                                      safeZoneCornerBotLeft, safeZoneCornerTopLeft):
        collisionUpperLeftCornerTemp, collisionUpperRightCornerTemp, collisionBottomLeftCornerTemp, collisionBottomRightCornerTemp = self.collisionDetector.detectCloserObstacleForEachCornerXAxis(
            collisionUpperRightCorner)
        if collisionBottomRightCornerTemp.positionY != self.MAP_SIZE_Y:
            endNode = self.__oneCollision_CollisionIsTop_noCollisionBeforeTheSideOfMap(collisionBottomRightCornerTemp,
                                            collisionUpperRightCorner, safeZoneCornerBotLeft, safeZoneCornerTopLeft)
        else:
            endNode = self.__oneCollision_CollisionIsTop_ThereIsCollisionBeforeTheSideOfMap(bottomRightCorner,
                                                        collisionBottomRightCorner, collisionUpperRightCorner)
        return endNode


    def __oneCollision_CollisionIsTop_ThereIsCollisionBeforeTheSideOfMap(self, bottomRightCorner,
                                        collisionBottomRightCorner, collisionUpperRightCorner):
        endNode = (Node((collisionUpperRightCorner.positionX + self.SAFE_MARGIN,
                         (collisionBottomRightCorner.positionY + collisionUpperRightCorner.positionY) / 2)))
        safeZoneCornerBotLeft = (bottomRightCorner[0], self.MAP_SIZE_Y - self.SAFE_MARGIN)
        safeZoneCornerTopRight = (collisionUpperRightCorner.positionX + self.SAFE_MARGIN,
                                  collisionUpperRightCorner.positionY + self.SAFE_MARGIN)
        safeZoneCornerTopLeft = (bottomRightCorner[0], collisionUpperRightCorner.positionY + self.SAFE_MARGIN)
        tempNode = self.graph.generateSafeZone(safeZoneCornerBotLeft, safeZoneCornerTopLeft, safeZoneCornerTopRight)
        self.graph.connectTwoNodes(endNode, tempNode)
        return endNode


    def __oneCollision_CollisionIsTop_noCollisionBeforeTheSideOfMap(self, collisionBottomRightCornerTemp,
                                                                    collisionUpperRightCorner, safeZoneCornerBotLeft,
                                                                    safeZoneCornerTopLeft):
        safeZoneCornerTopRight = (collisionBottomRightCornerTemp.positionX - self.SAFE_MARGIN,
                                  collisionUpperRightCorner.positionY + self.SAFE_MARGIN)
        safeZone = SafeZone(safeZoneCornerTopLeft, safeZoneCornerTopRight, safeZoneCornerBotLeft)
        endNode = safeZone.getCenterNodeOfSafeZone()
        self.graph.safeZonesList.append(safeZone)
        endNode.isASafeNode = True
        collisionBottomRightCornerTemp.setStartingNode(endNode)
        return endNode


    def __oneCollision_CollisionIsBottom(self, bottomRightCorner, collisionBottomRightCorner, collisionUpperRightCorner,
                                         safeZoneCornerBotLeft, safeZoneCornerTopLeft):
        collisionUpperLeftCornerTemp, collisionUpperRightCornerTemp, collisionBottomLeftCornerTemP, collisionBottomRightCornerTemp = self.collisionDetector.detectCloserObstacleForEachCornerXAxis(
                                                                                                                    collisionBottomRightCorner)
        if collisionUpperRightCornerTemp.positionY != 0:
            endNode = self.__ObstacleBetweenTheTwoCollision(
                collisionUpperRightCorner, collisionUpperRightCornerTemp, safeZoneCornerBotLeft,
                safeZoneCornerTopLeft)

        else:
            endNode = self.__oneCollision_CollisionIsBottom_noCollisionBeforeTheSideOfMap(bottomRightCorner,
                                                                                          collisionBottomRightCorner,
                                                                                          collisionUpperRightCorner)
        return endNode


    def __oneCollision_CollisionIsBottom_noCollisionBeforeTheSideOfMap(self, bottomRightCorner,
                                                             collisionBottomRightCorner, collisionUpperRightCorner):
        endNode = (Node((collisionBottomRightCorner.positionX + self.SAFE_MARGIN,
                         (collisionBottomRightCorner.positionY + collisionUpperRightCorner.positionY) / 2)))
        safeZoneCornerBotLeft = (bottomRightCorner[0], collisionBottomRightCorner.positionY - self.SAFE_MARGIN)
        safeZoneCornerTopRight = (collisionBottomRightCorner.positionX + self.SAFE_MARGIN, 0 + self.SAFE_MARGIN)
        safeZoneCornerTopLeft = (bottomRightCorner[0], 0 + self.SAFE_MARGIN)
        tempNode = self.graph.generateSafeZone(safeZoneCornerBotLeft, safeZoneCornerTopLeft, safeZoneCornerTopRight)
        self.graph.connectTwoNodes(endNode, tempNode)
        return endNode


    def __ObstacleBetweenTheTwoCollision(self, collisionUpperRightCorner,
                                         collisionUpperRightCornerTemp,
                                         safeZoneCornerBotLeft,
                                         safeZoneCornerTopLeft):
        safeZoneCornerTopRight = (collisionUpperRightCornerTemp.positionX - self.SAFE_MARGIN,
                                  collisionUpperRightCorner.positionY + self.SAFE_MARGIN)
        safeZone = SafeZone(safeZoneCornerTopLeft, safeZoneCornerTopRight, safeZoneCornerBotLeft)
        endNode = safeZone.getCenterNodeOfSafeZone()
        self.graph.safeZonesList.append(safeZone)
        collisionUpperRightCornerTemp.setStartingNode(endNode)
        endNode.isASafeNode = True
        return endNode
