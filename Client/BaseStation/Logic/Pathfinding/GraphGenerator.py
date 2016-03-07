from Client.BaseStation.Logic.Pathfinding.Node import Node
from Client.BaseStation.Logic.Pathfinding.SafeZone import SafeZone
from Client.BaseStation.Logic.Pathfinding.Obstacle import Obstacle
from Client.BaseStation.Logic.Pathfinding.EndNodeGenerator import EndNodeGenerator
from Client.BaseStation.Logic.Pathfinding.CollisionDetector import CollisionDetector
import numpy as np
import cv2

class GraphGenerator:
    MAP_SIZE_X = 1000
    MAP_SIZE_Y = 600
    SAFE_MARGIN = 30

    def __init__(self, obstaclesList):
        self.collisionDetector = CollisionDetector(self.MAP_SIZE_X, self.MAP_SIZE_Y, self.SAFE_MARGIN, obstaclesList)
        self.endNodeGenerator = EndNodeGenerator(self.MAP_SIZE_X, self.MAP_SIZE_Y, self.SAFE_MARGIN, obstaclesList, self.collisionDetector)
        self.obstaclesList = obstaclesList
        self.nodesList = []
        self.obstaclesList.sort(key=lambda obstacle: obstacle.positionX)


    def generateGraph(self):
        firstObstacle = self.obstaclesList[0]
        if (firstObstacle.positionX - self.SAFE_MARGIN > 0):
            startingNode = self.__defaultStart(firstObstacle)
            firstObstacle.setStartingNode(startingNode)
            compteur = 0

        else:
            #quand colle au mur en partant TO DO
            pass
            compteur = 1

        for compteur in range (compteur, self.obstaclesList.__len__()):
            currentObstacle = self.obstaclesList[(compteur)]

            startingNode = currentObstacle.startingNode
            topLeftCorner = (currentObstacle.positionX - self.SAFE_MARGIN, currentObstacle.positionY - self.SAFE_MARGIN)
            topRightCorner = (currentObstacle.positionX + self.SAFE_MARGIN, currentObstacle.positionY - self.SAFE_MARGIN)
            bottomRightCorner = (currentObstacle.positionX + self.SAFE_MARGIN, currentObstacle.positionY + self.SAFE_MARGIN)
            bottomLeftCorner = (currentObstacle.positionX - self.SAFE_MARGIN, currentObstacle.positionY + self.SAFE_MARGIN)
            collisionUpperLeftCorner, collisionUpperRightCorner, collisionBottomLeftCorner, collisionBottomRightCorner = self.collisionDetector.detectStackedObstacleXAxis(currentObstacle)

            borderNodeRightTop = self.__generateTopBracket(collisionUpperLeftCorner, collisionUpperRightCorner,
                                                           currentObstacle, startingNode, topLeftCorner, topRightCorner)
                
            borderNodeLeftBottom = Node((bottomLeftCorner[0], (bottomLeftCorner[1]+collisionBottomLeftCorner.positionY-self.SAFE_MARGIN)/2))
            self.__connectTwoNodes(startingNode,borderNodeLeftBottom)
            
            borderNodeRightBottom = Node((bottomRightCorner[0], (bottomRightCorner[1]+collisionBottomRightCorner.positionY-self.SAFE_MARGIN)/2))
            
            if(collisionBottomLeftCorner.positionY != self.MAP_SIZE_Y):
                tempNode = Node((collisionBottomLeftCorner.positionX + self.SAFE_MARGIN, (collisionBottomLeftCorner.positionY-self.SAFE_MARGIN + bottomLeftCorner[1])/2))
                self.__connectTwoNodes(borderNodeLeftBottom,tempNode)
            elif(collisionBottomRightCorner.positionY != self.MAP_SIZE_Y):

                collisionUpperLeftCornerTemp, collisionUpperRightCornerTemp, collisionBottomLeftCornerTemp, collisionBottomRightCornerTemp = self.collisionDetector.detectStackedObstacleXAxis(collisionBottomRightCorner)
                collisionGoodOne = collisionBottomRightCorner
                print "while Bottom"
                while collisionBottomLeftCornerTemp.positionY != self.MAP_SIZE_Y and collisionBottomLeftCornerTemp != collisionBottomLeftCorner:
                    collisionGoodOne = collisionBottomLeftCornerTemp
                    collisionUpperLeftCornerTemp, collisionUpperRightCornerTemp, collisionBottomLeftCornerTemp, collisionBottomRightCornerTemp = self.collisionDetector.detectStackedObstacleXAxis(collisionBottomLeftCornerTemp)
                    print compteur ,"goodOnebottom", collisionGoodOne.positionX, collisionGoodOne.positionY
                print "boba fett"
                print collisionGoodOne.positionX,collisionGoodOne.positionY
                tempNode = Node(((bottomLeftCorner[0]+collisionGoodOne.positionX-self.SAFE_MARGIN)/2,(bottomLeftCorner[1]+self.MAP_SIZE_Y-self.SAFE_MARGIN)/2))
                collisionGoodOne.setStartingNode(tempNode)
                self.__connectTwoNodes(borderNodeLeftBottom,tempNode)

            else:
                 self.__connectTwoNodes(borderNodeLeftBottom,borderNodeRightBottom)

            endNode = self.endNodeGenerator.generateEndNode(currentObstacle, topRightCorner, bottomRightCorner, collisionBottomRightCorner, collisionUpperRightCorner, compteur)
            self.__connectTwoNodes(borderNodeRightTop,endNode)
            self.__connectTwoNodes(borderNodeRightBottom,endNode)
            
        self.__displayGraph()

    def __generateTopBracket(self, collisionUpperLeftCorner, collisionUpperRightCorner, currentObstacle, startingNode,
                             topLeftCorner, topRightCorner):
        borderNodeLeftTop = Node(
            (topLeftCorner[0], (topLeftCorner[1] + collisionUpperLeftCorner.positionY + self.SAFE_MARGIN) / 2))
        self.__connectTwoNodes(startingNode, borderNodeLeftTop)
        borderNodeRightTop = Node(
            (topRightCorner[0], (topRightCorner[1] + collisionUpperRightCorner.positionY + self.SAFE_MARGIN) / 2))
        if (collisionUpperLeftCorner.positionY != 0):
            collisionUpperLeftCornerTemp, collisionUpperRightCornerTemp, collisionBottomLeftCornerTemp, collisionBottomRightCornerTemp = self.collisionDetector.detectStackedObstacleXAxis(
                collisionUpperLeftCorner)
            if collisionBottomRightCornerTemp == currentObstacle:
                tempNode = Node((collisionUpperLeftCorner.positionX + self.SAFE_MARGIN,
                                 (collisionUpperLeftCorner.positionY + self.SAFE_MARGIN + topLeftCorner[1]) / 2))
            else:
                goodCollision = collisionBottomRightCornerTemp
                collisionUpperLeftCornerTemp, collisionUpperRightCornerTemp, collisionBottomLeftCornerTemp, collisionBottomRightCornerTemp = self.collisionDetector.detectStackedObstacleXAxis(
                    goodCollision)
                while collisionBottomLeftCornerTemp != currentObstacle:
                    goodCollision = collisionBottomLeftCornerTemp
                    collisionUpperLeftCornerTemp, collisionUpperRightCornerTemp, collisionBottomLeftCornerTemp, collisionBottomRightCornerTemp = self.collisionDetector.detectStackedObstacleXAxis(
                        goodCollision)
                cornerTL = (topLeftCorner[0], collisionUpperLeftCorner.positionY + self.SAFE_MARGIN)
                cornerTR = (
                goodCollision.positionX - self.SAFE_MARGIN, collisionUpperLeftCorner.positionY + self.SAFE_MARGIN)
                cornerBL = (topLeftCorner[0], topLeftCorner[1])
                tempNode = Node(SafeZone(cornerTL, cornerTR, cornerBL).getCenterOfSafeZone())
                goodCollision.setStartingNode(tempNode)
            self.__connectTwoNodes(borderNodeLeftTop, tempNode)
        elif collisionUpperRightCorner.positionY != 0:
            collisionUpperRightCorner.setStartingNode(borderNodeLeftTop)

        else:
            self.__connectTwoNodes(borderNodeLeftTop, borderNodeRightTop)
        return borderNodeRightTop

    def __defaultStart(self, firstObstacle):
        cornerTL = (0, 0)
        cornerBL = (0, self.MAP_SIZE_Y)
        cornerTR = (firstObstacle.positionX - self.SAFE_MARGIN, cornerTL[1])
        nodeSafeZoneLeft = Node(SafeZone(cornerTL, cornerTR, cornerBL).getCenterOfSafeZone())
        return nodeSafeZoneLeft

    def __connectTwoNodes(self, firstNode, secondNode):
        firstNode, secondNode = self.__areNodesPresentInNodesList(firstNode, secondNode)
        firstNode.addConnectedNode(secondNode)
        secondNode.addConnectedNode(firstNode)

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

    def __displayGraph(self):
        img = np.zeros((600, 1000, 3), np.uint8)
        cv2.namedWindow('image')
        couleur = 0
        for compteur in range (0, self.obstaclesList.__len__()):
            currentObstacle = self.obstaclesList[(compteur)]
            cv2.rectangle(img, (currentObstacle.positionX - self.SAFE_MARGIN, currentObstacle.positionY - self.SAFE_MARGIN), (currentObstacle.positionX + self.SAFE_MARGIN, currentObstacle.positionY + self.SAFE_MARGIN),
                      (0, 255, 0), -1, 1)
            self.nodesList.sort(key=lambda node: node.positionX)
        for compteur in range (0, self.nodesList.__len__()):

            currentNode = self.nodesList[(compteur)]
            departPoint = (currentNode.positionX, currentNode.positionY)
            connectedNode = currentNode.getConnectedNodesList()
            for compteurConnected in range(0, connectedNode.__len__()):
                finalNode = connectedNode[(compteurConnected)]
                finalPoint = (finalNode.positionX, finalNode.positionY)
                cv2.line(img, departPoint, finalPoint,
                      (255, 0, 0), 2, 1)
        cv2.imshow('image', img)
        while (1):
            esc = cv2.waitKey(1)
            if esc == 27: #escape pressed
                break
        cv2.destroyAllWindows
listObs = []
listObs.append(Obstacle((180,200)))
listObs.append(Obstacle((220,300)))
listObs.append(Obstacle((240,100)))
listObs.append(Obstacle((280,220)))
listObs.append(Obstacle((340,400)))
listObs.append(Obstacle((330,100)))

listObs.append(Obstacle((215,400)))

listObs.append(Obstacle((700,350)))
listObs.append(Obstacle((190,500)))


bob = GraphGenerator (listObs)
bob.generateGraph()
