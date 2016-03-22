from Client.BaseStation.Logic.Pathfinding.LineInterceptionCalculator import LineInterceptionCalculator

class LineOfSightCalculator:
    def __init__(self, graph):
        self.lineInterceptionCalculator = LineInterceptionCalculator()
        self.graph = graph


    def tryStraightLine(self, goodPaths):
        for compteurPath in range(0, goodPaths.__len__()):
            currentPath = goodPaths[compteurPath]
            nodesToBeRemoved = []
            compteurNode = 0

            while compteurNode < currentPath.__len__():
                currentNode = currentPath[compteurNode]
                compteurFinalNode = currentPath.__len__()-1
                lineOfSight = False

                while compteurFinalNode > compteurNode+1:
                    finalNode = currentPath[compteurFinalNode]
                    lineOfSight = self.__nodesHasLineOfSight(currentNode, finalNode, lineOfSight)

                    if lineOfSight == True:
                        for compteurRemoved in range(compteurNode+1, compteurFinalNode):
                            nodesToBeRemoved.append(currentPath[compteurRemoved])
                        compteurNode = compteurFinalNode -1

                    compteurFinalNode += -1
                compteurNode += 1
            for compteurToBeRemoved in range(0, nodesToBeRemoved.__len__()):
                currentPath.remove(nodesToBeRemoved[compteurToBeRemoved])


    def __nodesHasLineOfSight(self, currentNode, finalNode, lineOfSight):
        topResult = True
        botResult = True
        leftResult = True
        rightResult = True
        for compteurObstacle in range(0, self.graph.obstaclesList.__len__() - 1):
            currentObstacle = self.graph.obstaclesList[compteurObstacle]
            pointA1 = (currentNode.positionX, currentNode.positionY)
            pointA2 = (finalNode.positionX, finalNode.positionY)

            topResult = self.__hasCollisionWithTopSideOfObstacle(topResult, currentObstacle, pointA1, pointA2)
            botResult = self.__hasCollisionWithBotSideOfObstacle(botResult, currentObstacle, pointA1, pointA2)
            leftResult = self.__hasCollisionWithLeftSideOfObstacle(currentObstacle, leftResult, pointA1, pointA2)
            rightResult = self.__hasCollisionWithRightSideOfObstacle(currentObstacle, pointA1, pointA2, rightResult)
        if topResult == True and botResult == True and leftResult == True and rightResult == True:
            lineOfSight = True
        return lineOfSight


    def __hasCollisionWithRightSideOfObstacle(self, currentObstacle, pointA1, pointA2, rightResult):
        pointB1 = (
        currentObstacle.positionX + self.graph.SAFE_MARGIN, currentObstacle.positionY - self.graph.SAFE_MARGIN)
        pointB2 = (
        currentObstacle.positionX + self.graph.SAFE_MARGIN, currentObstacle.positionY + self.graph.SAFE_MARGIN)
        intersection = self.lineInterceptionCalculator.findInterception(pointA1, pointA2, pointB1, pointB2)
        if intersection != False:
            if self.__isInYRange(intersection, pointA1, pointA2, pointB1, pointB2):
                rightResult = False
        return rightResult


    def __hasCollisionWithLeftSideOfObstacle(self, currentObstacle, leftResult, pointA1, pointA2):
        pointB1 = (
        currentObstacle.positionX - self.graph.SAFE_MARGIN, currentObstacle.positionY - self.graph.SAFE_MARGIN)
        pointB2 = (
        currentObstacle.positionX - self.graph.SAFE_MARGIN, currentObstacle.positionY + self.graph.SAFE_MARGIN)
        intersection = self.lineInterceptionCalculator.findInterception(pointA1, pointA2, pointB1, pointB2)
        if intersection != False:
            if self.__isInYRange(intersection, pointA1, pointA2, pointB1, pointB2):
                leftResult = False
        return leftResult


    def __hasCollisionWithBotSideOfObstacle(self, botResult, currentObstacle, pointA1, pointA2):
        pointB1 = (
        currentObstacle.positionX - self.graph.SAFE_MARGIN, currentObstacle.positionY + self.graph.SAFE_MARGIN)
        pointB2 = (
        currentObstacle.positionX + self.graph.SAFE_MARGIN, currentObstacle.positionY + self.graph.SAFE_MARGIN)
        intersection = self.lineInterceptionCalculator.findInterception(pointA1, pointA2, pointB1, pointB2)
        if intersection != False:
            if self.__isInXRange(intersection, pointA1, pointA2, pointB1, pointB2):
                botResult = False
        return botResult


    def __hasCollisionWithTopSideOfObstacle(self, topResult, currentObstacle, pointA1, pointA2):
        pointB1 = (currentObstacle.positionX - self.graph.SAFE_MARGIN, currentObstacle.positionY - self.graph.SAFE_MARGIN)
        pointB2 = (currentObstacle.positionX + self.graph.SAFE_MARGIN, currentObstacle.positionY - self.graph.SAFE_MARGIN)
        intersection = self.lineInterceptionCalculator.findInterception(pointA1, pointA2, pointB1, pointB2)
        if intersection != False:
            if self.__isInXRange(intersection, pointA1, pointA2, pointB1, pointB2):
                topResult = False
        return topResult


    def __isInXRange(self,intersection, pointA1, pointA2, pointB1, pointB2):
        return (intersection[0] < pointB2[0] and intersection[0] > pointB1[0]) and (
                    intersection[0] < pointA2[0] and intersection[0] > pointA1[0])


    def __isInYRange(self,intersection, pointA1, pointA2, pointB1, pointB2):
        return (intersection[1] < pointB2[1] and intersection[1] > pointB1[1]) and (
                    intersection[1] < pointA2[1] and intersection[1] > pointA1[1])

