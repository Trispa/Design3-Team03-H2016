from Client.BaseStation.Logic.Pathfinding.Graph.Node import Node

class BottomPathGenerator:
    def __init__(self, SAFE_MARGIN, MAP_SIZE_Y, graph, collisionDetector):
        self.SAFE_MARGIN = SAFE_MARGIN
        self.WALL_SAFE_MARGIN = SAFE_MARGIN - 25
        self. MAP_SIZE_Y = MAP_SIZE_Y
        self.graph = graph
        self.collisionDetector = collisionDetector


    def generateBottomPath(self, collisionBottomLeftCorner, collisionBottomRightCorner, currentObstacle,
                           borderNodeLeftBottom,
                           bottomLeftCorner, borderNodeRightBottom):
        goodRightCollision = self.__findGoodRightCollision(collisionBottomRightCorner, currentObstacle)
        resultInnerCollision, collidingObstacle = self.collisionDetector.hasLowerInnerCollision(currentObstacle)

        if collisionBottomLeftCorner.positionY == self.MAP_SIZE_Y and collisionBottomRightCorner.positionY == self.MAP_SIZE_Y:
            self.__obstacleIsNextToWall(borderNodeLeftBottom, borderNodeRightBottom, bottomLeftCorner,
                                        collisionBottomLeftCorner)
        elif (
                collisionBottomLeftCorner.positionY != self.MAP_SIZE_Y and collisionBottomRightCorner.positionY == self.MAP_SIZE_Y) or goodRightCollision.positionY >= collisionBottomLeftCorner.positionY or collidingObstacle.__contains__(collisionBottomLeftCorner):
            if resultInnerCollision == False:
                self.__collisionIsOnTheLeftSide(borderNodeLeftBottom, bottomLeftCorner, collisionBottomLeftCorner)
        else:
            self.__collisionIsOnTheRightSide(borderNodeLeftBottom, bottomLeftCorner, collisionBottomLeftCorner,
                                             goodRightCollision)


    def __collisionIsOnTheRightSide(self, borderNodeLeftBottom, bottomLeftCorner, collisionBottomLeftCorner,
                                    goodRightCollision):
        safeZoneCornerBotLeft = (bottomLeftCorner[0], collisionBottomLeftCorner.positionY - self.SAFE_MARGIN)
        safeZoneCornerTopRight = (goodRightCollision.positionX - self.SAFE_MARGIN, bottomLeftCorner[1])
        safeZoneCornerTopLeft = (bottomLeftCorner[0], bottomLeftCorner[1])
        tempNode = self.graph.generateSafeZone(safeZoneCornerBotLeft, safeZoneCornerTopLeft, safeZoneCornerTopRight)
        goodRightCollision.setStartingNode(tempNode)
        self.graph.connectTwoNodes(borderNodeLeftBottom, tempNode)


    def __collisionIsOnTheLeftSide(self, borderNodeLeftBottom, bottomLeftCorner, collisionBottomLeftCorner):
        tempNode = Node((collisionBottomLeftCorner.positionX + self.SAFE_MARGIN, borderNodeLeftBottom.positionY))
        safeZoneCornerBotLeft = (borderNodeLeftBottom.positionX, collisionBottomLeftCorner.positionY - self.SAFE_MARGIN)
        safeZoneCornerTopRight = (tempNode.positionX, bottomLeftCorner[1])
        safeZoneCornerTopLeft = (bottomLeftCorner[0], bottomLeftCorner[1])
        safeNode = self.graph.generateSafeZone(safeZoneCornerBotLeft, safeZoneCornerTopLeft, safeZoneCornerTopRight)
        self.graph.connectTwoNodes(borderNodeLeftBottom, safeNode)
        self.graph.connectTwoNodes(safeNode, tempNode)


    def __obstacleIsNextToWall(self, borderNodeLeftBottom, borderNodeRightBottom, bottomLeftCorner,
                               collisionBottomLeftCorner):
        safeZoneCornerBotLeft = (bottomLeftCorner[0], collisionBottomLeftCorner.positionY - self.WALL_SAFE_MARGIN)
        safeZoneCornerTopRight = (borderNodeRightBottom.positionX, bottomLeftCorner[1])
        safeZoneCornerTopLeft = (bottomLeftCorner[0], bottomLeftCorner[1])
        tempNode = self.graph.generateSafeZone(safeZoneCornerBotLeft, safeZoneCornerTopLeft, safeZoneCornerTopRight)
        self.graph.connectTwoNodes(borderNodeLeftBottom, tempNode)
        self.graph.connectTwoNodes(borderNodeRightBottom, tempNode)



    def __findGoodRightCollision(self, collisionBottomRightCorner, currentObstacle):
        goodRightCollision = collisionBottomRightCorner
        collisionUpperLeftCornerTemp, collisionUpperRightCornerTemp, collisionBottomLeftCornerTemp, collisionBottomRightCornerTemp = self.collisionDetector.detectCloserObstacleForEachCornerXAxis(
            goodRightCollision)
        while (
                            collisionUpperLeftCornerTemp == currentObstacle and collisionBottomLeftCornerTemp.positionY != self.MAP_SIZE_Y and collisionBottomLeftCornerTemp.positionX > currentObstacle.positionX):
            goodRightCollision = collisionBottomLeftCornerTemp

            collisionUpperLeftCornerTemp, collisionUpperRightCornerTemp, collisionBottomLeftCornerTemp, collisionBottomRightCornerTemp = self.collisionDetector.detectCloserObstacleForEachCornerXAxis(
                goodRightCollision)
        return goodRightCollision
