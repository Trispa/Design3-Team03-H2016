from Client.BaseStation.Logic.Pathfinding.Graph.Node import Node
from Client.BaseStation.Logic.Pathfinding.Graph.SafeZone import SafeZone

class Graph:
    def __init__(self, obstaclesList, safeMargin):
        self.SAFE_MARGIN = safeMargin
        self.nodesList = []
        self.obstaclesList =  obstaclesList
        self.safeZonesList = []


    def connectTwoNodes(self, firstNode, secondNode):
        firstNode, secondNode = self.__areNodesPresentInNodesList(firstNode, secondNode)
        firstNode.addConnectedNode(secondNode)
        secondNode.addConnectedNode(firstNode)


    def findGoodSafeNodeToGo(self, point):
        fakeNode = Node((0,0))
        nodeToBeReturned = fakeNode
        for compteur in range(0, self.safeZonesList.__len__()):
            currentZone = self.safeZonesList[compteur]
            if point[0] >= currentZone.cornerTopLeft[0] and point[0] <= currentZone.cornerBottomRight[0]:
                if point[1] >= currentZone.cornerTopLeft[1] and point[1] <= currentZone.cornerBottomRight[1]:
                    nodeToBeReturned = currentZone.centerNode
        return nodeToBeReturned


    def needAGoodPointToGo(self, point):
        fakePoint = (0,0)
        pointToBeReturned = fakePoint
        for compteur in range(0, self.safeZonesList.__len__()):
            currentZone = self.safeZonesList[compteur]
            if point[0] >= currentZone.cornerTopLeft[0] and point[0] <= currentZone.cornerBottomRight[0]:
                if point[1] >= currentZone.cornerTopLeft[1] and point[1] <= currentZone.cornerBottomRight[1]:
                    pointToBeReturned = (currentZone.centerNode.positionX, currentZone.centerNode.positionY)
        if pointToBeReturned == fakePoint:
            buffer = 5
            while pointToBeReturned[0] == 0 and pointToBeReturned[1] == 0:
                for xIteration in range (-1,2):
                    for yIteration in range(-1,2):
                        pointX = point[0] + buffer*xIteration
                        pointY = point[1] + buffer*yIteration
                        if pointToBeReturned[0] == 0 and pointToBeReturned[1] == 0:
                            centerNode = self.findGoodSafeNodeToGo((pointX,pointY))
                            if centerNode.positionX != 0 and centerNode.positionY != 1:
                                pointToBeReturned = (centerNode.positionX, centerNode.positionY)
                buffer += 5
        return pointToBeReturned


    def needAClosePoint(self, point):
        fakePoint = (0,0)
        pointToBeReturned = fakePoint
        for compteur in range(0, self.safeZonesList.__len__()):
            currentZone = self.safeZonesList[compteur]
            if point[0] >= currentZone.cornerTopLeft[0] and point[0] <= currentZone.cornerBottomRight[0]:
                if point[1] >= currentZone.cornerTopLeft[1] and point[1] <= currentZone.cornerBottomRight[1]:
                    pointToBeReturned = point
        if pointToBeReturned == fakePoint:
            buffer = 5
            while pointToBeReturned[0] == 0 and pointToBeReturned[1] == 0 and buffer <= 15:
                for xIteration in range (-1,2):
                    for yIteration in range(-1,2):
                        pointX = point[0] + buffer*xIteration
                        pointY = point[1] + buffer*yIteration
                        if pointToBeReturned[0] == 0 and pointToBeReturned[1] == 0:
                            centerNode = self.findGoodSafeNodeToGo((pointX,pointY))
                            if centerNode.positionX != 0 and centerNode.positionY != 1:
                                pointToBeReturned = (pointX, pointY)
                buffer += 5
        if pointToBeReturned == fakePoint:
            return point
        return pointToBeReturned


    def __areNodesPresentInNodesList(self, firstNode, secondNode):
        toBeAddFirst = True
        toBeAddSecond = True
        for compteur in range(0, self.nodesList.__len__()):
            currentNode = self.nodesList[(compteur)]
            if (firstNode.positionX == currentNode.positionX and firstNode.positionY == currentNode.positionY):
                firstNode = currentNode
                toBeAddFirst = False
            elif (secondNode.positionX == currentNode.positionX and secondNode.positionY == currentNode.positionY):
                secondNode = currentNode
                toBeAddSecond = False
        if toBeAddFirst == True:
            self.nodesList.append(firstNode)
        if toBeAddSecond == True:
            self.nodesList.append(secondNode)
        return firstNode, secondNode


    def generateSafeZone(self, safeZoneCornerBotLeft, safeZoneCornerTopLeft, safeZoneCornerTopRight):
        safeZone = SafeZone(safeZoneCornerTopLeft, safeZoneCornerTopRight, safeZoneCornerBotLeft)
        tempNode = safeZone.getCenterNodeOfSafeZone()
        self.safeZonesList.append(safeZone)
        tempNode.isASafeNode = True
        return tempNode


    def __len__(self):
        return self.nodesList.__len__()