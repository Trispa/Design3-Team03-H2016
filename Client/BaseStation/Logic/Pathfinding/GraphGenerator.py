from Client.BaseStation.Logic.Pathfinding.Node import Node
from Client.BaseStation.Logic.Pathfinding.SafeZone import SafeZone
import numpy as np
import cv2

class GraphGenerator:
    MAP_SIZE_X = 1000
    MAP_SIZE_Y = 600
    SAFE_MARGIN = 20

    def __init__(self, obstaclesList):
        self.obstaclesList = obstaclesList
        self.nodesList = []
        self.obstaclesList.sort()


    def generateGraph(self):
        cornerTL = (0,0)
        cornerBL = (0, self.MAP_SIZE_Y)
        cornerTR = (self.obstaclesList.__getitem__(0).__getitem__(0) - self.SAFE_MARGIN, cornerTL.__getitem__(1))
        nodeSafeZoneLeft = Node(SafeZone(cornerTL, cornerTR, cornerBL).getCenterOfSafeZone())

        for compteur in range (0, self.obstaclesList.__len__()):
            currentObstacle = self.obstaclesList.__getitem__(compteur)
            topLeftCorner = (currentObstacle.__getitem__(0) - self.SAFE_MARGIN, currentObstacle.__getitem__(1) - self.SAFE_MARGIN)
            topRightCorner = (currentObstacle.__getitem__(0) + self.SAFE_MARGIN, currentObstacle.__getitem__(1) - self.SAFE_MARGIN)
            bottomRightCorner = (currentObstacle.__getitem__(0) + self.SAFE_MARGIN, currentObstacle.__getitem__(1) + self.SAFE_MARGIN)
            bottomLeftCorner = (currentObstacle.__getitem__(0) - self.SAFE_MARGIN, currentObstacle.__getitem__(1) + self.SAFE_MARGIN)
            Corners = [topLeftCorner, topRightCorner, bottomLeftCorner, bottomRightCorner]

            cornerTR = (topLeftCorner.__getitem__(0), cornerTL.__getitem__(1))
            borderNodeLeftTop = Node((topLeftCorner.__getitem__(0), topLeftCorner.__getitem__(1)/2))
            borderNodeLeftDown = Node((bottomLeftCorner.__getitem__(0), (bottomLeftCorner.__getitem__(1)+self.MAP_SIZE_Y)/2))
            self.__connectTwoNodes(nodeSafeZoneLeft,borderNodeLeftTop)
            self.__connectTwoNodes(nodeSafeZoneLeft,borderNodeLeftDown)

            if (compteur == self.obstaclesList.__len__()-1):
                cornerTR = (self.MAP_SIZE_X,0)
            elif (self.obstaclesList.__getitem__(compteur+1).__getitem__(0) > currentObstacle.__getitem__(0) + self.SAFE_MARGIN):
                cornerTR = (self.obstaclesList.__getitem__(compteur+1).__getitem__(0),0)
            else:
                pass
            borderNodeRightTop = Node((topRightCorner.__getitem__(0), topRightCorner.__getitem__(1)/2))
            borderNodeRightDown = Node((bottomRightCorner.__getitem__(0), (bottomRightCorner.__getitem__(1)+self.MAP_SIZE_Y)/2))
            self.__connectTwoNodes(borderNodeLeftTop,borderNodeRightTop)
            self.__connectTwoNodes(borderNodeLeftDown, borderNodeRightDown)
            cornerTL = (borderNodeRightDown.positionX,0)
            cornerBL = (borderNodeRightDown, self.MAP_SIZE_Y)
            nodeSafeZoneRight = Node(SafeZone(cornerTL, cornerTR, cornerBL).getCenterOfSafeZone())
            self.__connectTwoNodes(borderNodeRightTop, nodeSafeZoneRight)
            self.__connectTwoNodes(borderNodeRightDown, nodeSafeZoneRight)
            nodeSafeZoneLeft = nodeSafeZoneRight
        self.__displayGraph()

    def __connectTwoNodes(self, firstNode, secondNode):
        firstNode, secondNode = self.__areNodesPresentInNodesList(firstNode, secondNode)
        firstNode.addConnectedNode(secondNode)
        secondNode.addConnectedNode(firstNode)

    def __areNodesPresentInNodesList(self, firstNode, secondNode):
        toBeAddFirst = True
        toBeAddSecond = True
        for compteur in range(0, self.nodesList.__len__()):
            currentNode = self.nodesList.__getitem__(compteur)
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

    def __displayGraph(self):
        img = np.zeros((600, 1000, 3), np.uint8)
        cv2.namedWindow('image')
        for compteur in range (0, self.obstaclesList.__len__()):
            currentObstacle = self.obstaclesList.__getitem__(compteur)
            cv2.rectangle(img, (currentObstacle.__getitem__(0) - 20, currentObstacle.__getitem__(1) - 20), (currentObstacle.__getitem__(0) + 20, currentObstacle.__getitem__(1) + 20),
                      (0, 255, 0), -1, 1)
        for compteur in range (0, self.nodesList.__len__()):
            currentNode = self.nodesList.__getitem__(compteur)
            departPoint = (currentNode.positionX, currentNode.positionY)
            print departPoint
            connectedNode = currentNode.getConnectedNodesList()
            for compteurConnected in range(0, connectedNode.__len__()):
                finalNode = connectedNode.__getitem__(compteurConnected)
                finalPoint = (finalNode.positionX, finalNode.positionY)
                cv2.line(img, departPoint, finalPoint,
                      (255, 0, 0), 3, 1)
        cv2.imshow('image', img)
        while (1):
            esc = cv2.waitKey(1)
            if esc == 27: #escape pressed
                break
        cv2.destroyAllWindows

bob = GraphGenerator ([(100,100), (300,300), (500,500)])
bob.generateGraph()
