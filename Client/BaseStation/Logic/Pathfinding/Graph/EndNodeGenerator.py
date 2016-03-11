from Client.BaseStation.Logic.Pathfinding.Graph.Node import Node
from Client.BaseStation.Logic.Pathfinding.Graph.SafeZone import SafeZone


class EndNodeGenerator:
    def __init__(self, mapSizeX, mapSizeY, safeMargin, obstacleList, collisionDetector):
        self.MAP_SIZE_X = mapSizeX
        self.MAP_SIZE_Y = mapSizeY
        self.SAFE_MARGIN = safeMargin
        self.collisionDetector = collisionDetector
        self.obstaclesList = obstacleList

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
        safeZoneCornerTopLeft = (currentObstacle.positionX + self.SAFE_MARGIN, 0)
        safeZoneCornerBotLeft = (currentObstacle.positionX + self.SAFE_MARGIN, self.MAP_SIZE_Y)
        if (compteur == self.obstaclesList.__len__() - 1):
            safeZoneCornerTopRight = (self.MAP_SIZE_X, 0)
            endNode = Node(SafeZone(safeZoneCornerTopLeft, safeZoneCornerTopRight, safeZoneCornerBotLeft).getCenterOfSafeZone())
        else:
            safeZoneCornerTopRight = (self.obstaclesList[compteur + 1].positionX - self.SAFE_MARGIN, 0)
            endNode = Node(SafeZone(safeZoneCornerTopLeft, safeZoneCornerTopRight, safeZoneCornerBotLeft).getCenterOfSafeZone())
            self.obstaclesList[compteur+1].setStartingNode(endNode)

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
                endNode = Node(SafeZone(safeZoneCornerTopLeft, safeZoneCornerTopRight, safeZoneCornerBotLeft).getCenterOfSafeZone())
                collisionUpperRightCornerTemp.setStartingNode(endNode)

            else:
                endNode = (Node((collisionBottomRightCorner.positionX + self.SAFE_MARGIN,
                                 (collisionBottomRightCorner.positionY + collisionUpperRightCorner.positionY) / 2)))

        else:
            collisionUpperLeftCornerTemp, collisionUpperRightCornerTemp, collisionBottomLeftCornerTemp, collisionBottomRightCornerTemp = self.collisionDetector.detectStackedObstacleXAxis(
                collisionUpperRightCorner)

            if collisionBottomRightCornerTemp != collisionBottomRightCorner:
                safeZoneCornerTopRight = (collisionBottomRightCornerTemp.positionX - self.SAFE_MARGIN,
                            collisionUpperRightCorner.positionY + self.SAFE_MARGIN)
                endNode = Node(SafeZone(safeZoneCornerTopLeft, safeZoneCornerTopRight, safeZoneCornerBotLeft).getCenterOfSafeZone())
                collisionBottomRightCornerTemp.setStartingNode(endNode)

            else:
                endNode = (Node((collisionUpperRightCorner.positionX + self.SAFE_MARGIN,
                                 (collisionBottomRightCorner.positionY + collisionUpperRightCorner.positionY) / 2)))
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
                endNode = Node(SafeZone(safeZoneCornerTopLeft, safeZoneCornerTopRight, safeZoneCornerBotLeft).getCenterOfSafeZone())
                collisionUpperRightCornerTemp.setStartingNode(endNode)

            else:
                endNode = (Node((collisionBottomRightCorner.positionX + self.SAFE_MARGIN,
                                 (collisionBottomRightCorner.positionY + collisionUpperRightCorner.positionY) / 2)))

        else:
            collisionUpperLeftCornerTemp, collisionUpperRightCornerTemp, collisionBottomLeftCornerTemp, collisionBottomRightCornerTemp = self.collisionDetector.detectStackedObstacleXAxis(
                collisionUpperRightCorner)

            if collisionBottomRightCornerTemp.positionY != self.MAP_SIZE_Y:
                safeZoneCornerTopRight = (collisionBottomRightCornerTemp.positionX - self.SAFE_MARGIN,
                            collisionUpperRightCorner.positionY + self.SAFE_MARGIN)
                endNode = Node(SafeZone(safeZoneCornerTopLeft, safeZoneCornerTopRight, safeZoneCornerBotLeft).getCenterOfSafeZone())
                collisionBottomRightCornerTemp.setStartingNode(endNode)

            else:
                endNode = (Node((collisionUpperRightCorner.positionX + self.SAFE_MARGIN,
                                 (collisionBottomRightCorner.positionY + collisionUpperRightCorner.positionY) / 2)))
        return endNode

