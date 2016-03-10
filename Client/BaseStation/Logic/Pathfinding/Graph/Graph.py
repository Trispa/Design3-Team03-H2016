from Client.BaseStation.Logic.Pathfinding.Graph.Node import Node
import numpy as np
class Graph:
    def __init__(self, obstaclesList):
        self.nodesList = []
        self.obstaclesList = obstaclesList


    def connectTwoNodes(self, firstNode, secondNode):
        firstNode, secondNode = self.__areNodesPresentInNodesList(firstNode, secondNode)
        firstNode.addConnectedNode(secondNode)
        secondNode.addConnectedNode(firstNode)

    def findClosestNodeTo(self, point):
        distance = 9999
        nodeToBeReturned = Node((0,0))
        for compteur in range(0, self.nodesList.__len__()):
            currentNode = self.nodesList[compteur]
            distanceNode = np.sqrt(np.power((currentNode.positionX - point[0]),2)+np.power((currentNode.positionY - point[1]),2))
            if distanceNode < distance:
                distance = distanceNode
                nodeToBeReturned = currentNode
        return nodeToBeReturned


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

    def __len__(self):
        return self.nodeList.__len__()