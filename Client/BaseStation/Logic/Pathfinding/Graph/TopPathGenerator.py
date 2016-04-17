from Client.BaseStation.Logic.Pathfinding.Graph.Node import Node

class TopPathGenerator:
    def __init__(self, SAFE_MARGIN, MAP_SIZE_Y, graph, collisionDetector):
        self.SAFE_MARGIN = SAFE_MARGIN
        self.WALL_SAFE_MARGIN = SAFE_MARGIN - 25
        self.MAP_SIZE_Y = MAP_SIZE_Y
        self.graph = graph
        self.collisionDetector = collisionDetector


    def generateTopPath(self, collisionUpperLeftCorner, collisionUpperRightCorner, currentObstacle, borderNodeLeftTop,
                          topLeftCorner, borderNodeRightTop):
        goodRightCollision = self.__findGoodRightCollision(collisionUpperRightCorner, currentObstacle)
        resultInnerCollision, collidingObstacle = self.collisionDetector.hasUpperInnerCollision(currentObstacle)

        if collisionUpperLeftCorner.positionY == 0 and collisionUpperRightCorner.positionY == 0:
            self.__obstacleIsNextToWall(borderNodeLeftTop, borderNodeRightTop, collisionUpperLeftCorner, topLeftCorner)

        elif (
                collisionUpperLeftCorner.positionY != 0 and collisionUpperRightCorner.positionY == 0) or (goodRightCollision.positionY <= collisionUpperLeftCorner.positionY) or (collidingObstacle.__contains__(collisionUpperLeftCorner)):
            if resultInnerCollision == False:
                self.__CollisionOnTheLeftSide(borderNodeLeftTop, collisionUpperLeftCorner, topLeftCorner)
        else:
            self.__collisionOnTheRightSide(borderNodeLeftTop, collisionUpperLeftCorner, goodRightCollision,
                                           topLeftCorner)


    def __collisionOnTheRightSide(self, borderNodeLeftTop, collisionUpperLeftCorner, goodRightCollision, topLeftCorner):
        safeZoneCornerTopLeft = (topLeftCorner[0], collisionUpperLeftCorner.positionY + self.SAFE_MARGIN)
        safeZoneCornerTopRight = (
            goodRightCollision.positionX - self.SAFE_MARGIN, collisionUpperLeftCorner.positionY + self.SAFE_MARGIN)
        safeZoneCornerBotLeft = (topLeftCorner[0], topLeftCorner[1])
        tempNode = self.graph.generateSafeZone(safeZoneCornerBotLeft, safeZoneCornerTopLeft, safeZoneCornerTopRight)
        goodRightCollision.setStartingNode(tempNode)
        self.graph.connectTwoNodes(borderNodeLeftTop, tempNode)


    def __CollisionOnTheLeftSide(self, borderNodeLeftTop, collisionUpperLeftCorner, topLeftCorner):
        tempNode = Node((collisionUpperLeftCorner.positionX + self.SAFE_MARGIN, borderNodeLeftTop.positionY))
        safeZoneCornerBotLeft = (borderNodeLeftTop.positionX, topLeftCorner[1])
        safeZoneCornerTopRight = (tempNode.positionX, collisionUpperLeftCorner.positionY + self.SAFE_MARGIN)
        safeZoneCornerTopLeft = (borderNodeLeftTop.positionX, collisionUpperLeftCorner.positionY + self.SAFE_MARGIN)
        safeNode = self.graph.generateSafeZone(safeZoneCornerBotLeft, safeZoneCornerTopLeft, safeZoneCornerTopRight)
        self.graph.connectTwoNodes(borderNodeLeftTop, safeNode)
        self.graph.connectTwoNodes(safeNode, tempNode)


    def __obstacleIsNextToWall(self, borderNodeLeftTop, borderNodeRightTop, collisionUpperLeftCorner, topLeftCorner):
        if topLeftCorner[0] <= 60:
            safeZoneCornerTopLeft = (60, collisionUpperLeftCorner.positionY + self.WALL_SAFE_MARGIN)
            safeZoneCornerBotLeft = (60, topLeftCorner[1])
        else:
            safeZoneCornerTopLeft = (topLeftCorner[0], collisionUpperLeftCorner.positionY + self.WALL_SAFE_MARGIN)
            safeZoneCornerBotLeft = (topLeftCorner[0], topLeftCorner[1])
        safeZoneCornerTopRight = (borderNodeRightTop.positionX, collisionUpperLeftCorner.positionY + self.WALL_SAFE_MARGIN)
        tempNode = self.graph.generateSafeZone(safeZoneCornerBotLeft, safeZoneCornerTopLeft, safeZoneCornerTopRight)
        self.graph.connectTwoNodes(borderNodeLeftTop, tempNode)
        self.graph.connectTwoNodes(borderNodeRightTop, tempNode)


    def __findGoodRightCollision(self, collisionUpperRightCorner, currentObstacle):
        goodRightCollision = collisionUpperRightCorner
        collisionUpperLeftCornerTemp, collisionUpperRightCornerTemp, collisionBottomLeftCornerTemp, collisionBottomRightCornerTemp = self.collisionDetector.detectCloserObstacleForEachCornerXAxis(
            goodRightCollision)
        while (
                            collisionBottomLeftCornerTemp == currentObstacle and collisionUpperLeftCornerTemp.positionY != 0 and collisionUpperLeftCornerTemp.positionX > currentObstacle.positionX):
            goodRightCollision = collisionUpperLeftCornerTemp

            collisionUpperLeftCornerTemp, collisionUpperRightCornerTemp, collisionBottomLeftCornerTemp, collisionBottomRightCornerTemp = self.collisionDetector.detectCloserObstacleForEachCornerXAxis(
                goodRightCollision)
        return goodRightCollision