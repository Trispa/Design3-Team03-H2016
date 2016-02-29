from Client.BaseStation.Logic.Pathfinding.Node import Node
from Client.BaseStation.Logic.Pathfinding.SafeZone import SafeZone
from Client.BaseStation.Logic.Pathfinding.Obstacle import Obstacle
import numpy as np
import cv2

class GraphGenerator:
    MAP_SIZE_X = 1000
    MAP_SIZE_Y = 600
    SAFE_MARGIN = 30

    def __init__(self, obstaclesList):
        self.obstaclesList = obstaclesList
        self.nodesList = []
        self.obstaclesList.sort(key=lambda obstacle: obstacle.positionX)
        for compteur in range (0, self.obstaclesList.__len__()):
            print obstaclesList[compteur].positionX


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
            if (startingNode.positionX == 0 and startingNode.positionY == 0):
                startingNode = endNode
            topLeftCorner = (currentObstacle.positionX - self.SAFE_MARGIN, currentObstacle.positionY - self.SAFE_MARGIN)
            topRightCorner = (currentObstacle.positionX + self.SAFE_MARGIN, currentObstacle.positionY - self.SAFE_MARGIN)
            bottomRightCorner = (currentObstacle.positionX + self.SAFE_MARGIN, currentObstacle.positionY + self.SAFE_MARGIN)
            bottomLeftCorner = (currentObstacle.positionX - self.SAFE_MARGIN, currentObstacle.positionY + self.SAFE_MARGIN)
            collisionUpperLeftCorner, collisionUpperRightCorner, collisionBottomLeftCorner, collisionBottomRightCorner = self.__detectStackedObstacleXAxis(currentObstacle)

            if (collisionBottomRightCorner.positionY != self.MAP_SIZE_Y and collisionUpperRightCorner.positionY != 0):
                if (collisionBottomRightCorner.positionX < collisionUpperRightCorner.positionX):
                    collisionUpperLeftCornerTemp, collisionUpperRightCornerTemp, collisionBottomLeftCornerTemP, collisionBottomRightCornerTemp = self.__detectStackedObstacleXAxis(collisionBottomRightCorner)
                    endNode = Node((collisionBottomRightCorner.positionX+self.SAFE_MARGIN,(collisionBottomRightCorner.positionY+collisionUpperRightCornerTemp.positionY)/2))
                else:
                    collisionUpperLeftCornerTemp, collisionUpperRightCornerTemp, collisionBottomLeftCornerTemp, collisionBottomRightCornerTemp = self.__detectStackedObstacleXAxis(collisionUpperRightCorner)
                    endNode = Node((collisionUpperRightCorner.positionX+self.SAFE_MARGIN,(collisionUpperRightCorner.positionY+collisionBottomRightCornerTemp.positionY)/2))

            borderNodeLeftTop = Node((topLeftCorner[0], (topLeftCorner[1]+collisionUpperLeftCorner.positionY+self.SAFE_MARGIN)/2))
            self.__connectTwoNodes(startingNode,borderNodeLeftTop)
            
            borderNodeRightTop = Node((topRightCorner[0], (topRightCorner[1]+collisionUpperRightCorner.positionY+self.SAFE_MARGIN)/2))
            
            if(collisionUpperLeftCorner.positionY != 0):
                tempNode = Node((collisionUpperLeftCorner.positionX + self.SAFE_MARGIN, (collisionUpperLeftCorner.positionY+self.SAFE_MARGIN + topLeftCorner[1])/2))
                self.__connectTwoNodes(borderNodeLeftTop,tempNode)
            elif(collisionUpperRightCorner.positionY != 0):
                if collisionUpperLeftCorner.positionY == 0:
                    tempNode = Node(((topLeftCorner[0]+collisionUpperRightCorner.positionX-self.SAFE_MARGIN)/2,topLeftCorner[1]/2))
                    collisionUpperRightCorner.setStartingNode(tempNode)
                    self.__connectTwoNodes(borderNodeLeftTop,tempNode)
                    
                if (collisionUpperRightCorner.positionX <= collisionBottomRightCorner.positionX):
                    collisionUpperLeftCornerTemp, collisionUpperRightCornerTemp, collisionBottomLeftCornerTemp, collisionBottomRightCornerTemp = self.__detectStackedObstacleXAxis(collisionUpperRightCorner)
                    if collisionBottomRightCornerTemp.positionY != self.MAP_SIZE_Y and collisionBottomRightCornerTemp != collisionBottomRightCorner:
                        print compteur
                        print 'bob'
                        cornerTL = (topRightCorner[0], collisionUpperRightCorner.positionY+self.SAFE_MARGIN)
                        cornerTR = (collisionBottomRightCornerTemp.positionX-self.SAFE_MARGIN, collisionUpperRightCorner.positionY+self.SAFE_MARGIN)
                        cornerBL = (bottomRightCorner[0], collisionBottomRightCorner.positionY-self.SAFE_MARGIN)
                        endNode = Node(SafeZone(cornerTL,cornerTR,cornerBL).getCenterOfSafeZone())
                        collisionBottomRightCornerTemp.setStartingNode(endNode)
                    else :
                        endNode = Node((collisionUpperRightCorner.positionX+self.SAFE_MARGIN,(collisionUpperRightCorner.positionY+collisionBottomRightCornerTemp.positionY)/2))
            else:
                self.__connectTwoNodes(borderNodeLeftTop,borderNodeRightTop)
                
            borderNodeLeftBottom = Node((bottomLeftCorner[0], (bottomLeftCorner[1]+collisionBottomLeftCorner.positionY-self.SAFE_MARGIN)/2))
            self.__connectTwoNodes(startingNode,borderNodeLeftBottom)
            
            borderNodeRightBottom = Node((bottomRightCorner[0], (bottomRightCorner[1]+collisionBottomRightCorner.positionY-self.SAFE_MARGIN)/2))
            
            if(collisionBottomLeftCorner.positionY != self.MAP_SIZE_Y):
                tempNode = Node((collisionBottomLeftCorner.positionX + self.SAFE_MARGIN, (collisionBottomLeftCorner.positionY-self.SAFE_MARGIN + bottomLeftCorner[1])/2))
                self.__connectTwoNodes(borderNodeLeftBottom,tempNode)
            elif(collisionBottomRightCorner.positionY != self.MAP_SIZE_Y):
                if collisionBottomLeftCorner.positionY == self.MAP_SIZE_Y:
                    tempNode = Node(((bottomLeftCorner[0]+collisionBottomRightCorner.positionX-self.SAFE_MARGIN)/2,(bottomLeftCorner[1]+self.MAP_SIZE_Y-self.SAFE_MARGIN)/2))
                    collisionBottomRightCorner.setStartingNode(tempNode)
                    self.__connectTwoNodes(borderNodeLeftBottom,tempNode)
                    
                if (collisionBottomRightCorner.positionX < collisionUpperRightCorner.positionX):
                    collisionUpperLeftCornerTemp, collisionUpperRightCornerTemp, collisionBottomLeftCornerTemP, collisionBottomRightCornerTemp = self.__detectStackedObstacleXAxis(collisionBottomRightCorner)
                    if collisionUpperRightCornerTemp.positionY != 0 and collisionUpperRightCornerTemp != collisionUpperRightCorner:
                        print compteur
                        cornerTL = (topRightCorner[0], collisionUpperRightCorner.positionY+self.SAFE_MARGIN)
                        cornerTR = (collisionUpperRightCornerTemp.positionX-self.SAFE_MARGIN, collisionUpperRightCorner.positionY+self.SAFE_MARGIN)
                        cornerBL = (bottomRightCorner[0], collisionBottomRightCorner.positionY-self.SAFE_MARGIN)
                        endNode = Node(SafeZone(cornerTL,cornerTR,cornerBL).getCenterOfSafeZone())
                        collisionUpperRightCornerTemp.setStartingNode(endNode)
                    else :
                        endNode = Node((collisionBottomRightCorner.positionX+self.SAFE_MARGIN,(collisionBottomRightCorner.positionY+collisionUpperRightCornerTemp.positionY)/2))
            else:
                 self.__connectTwoNodes(borderNodeLeftBottom,borderNodeRightBottom)
            if (collisionBottomRightCorner.positionY == self.MAP_SIZE_Y and collisionUpperRightCorner.positionY != 0):
                collisionUpperLeftCornerTemp, collisionUpperRightCornerTemp, collisionBottomLeftCornerTemp, collisionBottomRightCornerTemp = self.__detectStackedObstacleXAxis(collisionUpperRightCorner)
                if collisionBottomRightCornerTemp.positionY != self.MAP_SIZE_Y:

                    cornerTL = (topRightCorner[0], collisionUpperRightCorner.positionY+self.SAFE_MARGIN)
                    cornerTR = (collisionBottomRightCornerTemp.positionX-self.SAFE_MARGIN, collisionUpperRightCorner.positionY+self.SAFE_MARGIN)
                    cornerBL = (bottomRightCorner[0], collisionBottomRightCorner.positionY-self.SAFE_MARGIN)
                    endNode = Node(SafeZone(cornerTL,cornerTR,cornerBL).getCenterOfSafeZone())
                    collisionBottomRightCornerTemp.setStartingNode(endNode)
                else :
                    endNode = Node((collisionUpperRightCorner.positionX+self.SAFE_MARGIN,(collisionUpperRightCorner.positionY+collisionBottomRightCornerTemp.positionY)/2))


            if (collisionBottomRightCorner.positionY != self.MAP_SIZE_Y and collisionUpperRightCorner.positionY == 0):
                collisionUpperLeftCornerTemp, collisionUpperRightCornerTemp, collisionBottomLeftCornerTemP, collisionBottomRightCornerTemp = self.__detectStackedObstacleXAxis(collisionBottomRightCorner)
                if collisionUpperRightCornerTemp.positionY != 0:
                    cornerTL = (topRightCorner[0], collisionUpperRightCorner.positionY+self.SAFE_MARGIN)
                    cornerTR = (collisionUpperRightCornerTemp.positionX-self.SAFE_MARGIN, collisionUpperRightCorner.positionY+self.SAFE_MARGIN)
                    cornerBL = (bottomRightCorner[0], collisionBottomRightCorner.positionY-self.SAFE_MARGIN)
                    endNode = Node(SafeZone(cornerTL,cornerTR,cornerBL).getCenterOfSafeZone())
                    collisionUpperRightCornerTemp.setStartingNode(endNode)
                else :
                    endNode = Node((collisionBottomRightCorner.positionX+self.SAFE_MARGIN,(collisionBottomRightCorner.positionY+collisionUpperRightCornerTemp.positionY)/2))

            if (collisionBottomRightCorner.positionY == self.MAP_SIZE_Y and collisionUpperRightCorner.positionY == 0):
                cornerTL = (borderNodeRightTop.positionX, 0)
                cornerBL = (borderNodeRightBottom.positionX, self.MAP_SIZE_Y)
                if(compteur == self.obstaclesList.__len__() - 1):
                    cornerTR = (self.MAP_SIZE_X,0)
                else:
                    cornerTR = (self.obstaclesList[compteur+1].positionX-self.SAFE_MARGIN,0)
                endNode =  Node(SafeZone(cornerTL, cornerTR, cornerBL).getCenterOfSafeZone())
            self.__connectTwoNodes(borderNodeRightTop,endNode)
            self.__connectTwoNodes(borderNodeRightBottom,endNode)
            
        self.__displayGraph()


    def __detectStackedObstacleXAxis(self, verifiedObstacle):
        collisionUpperLeftCorner = Obstacle((verifiedObstacle.positionX, 0))
        collisionUpperRightCorner = Obstacle((verifiedObstacle.positionX, 0))
        collisionBottomLeftCorner = Obstacle((verifiedObstacle.positionX, self.MAP_SIZE_Y))
        collisionBottomRightCorner = Obstacle((verifiedObstacle.positionX, self.MAP_SIZE_Y))
        for compteur in range(0, self.obstaclesList.__len__()):
            currentObstacle = self.obstaclesList[compteur]
            if currentObstacle != verifiedObstacle:
                if (verifiedObstacle.positionX - 2*self.SAFE_MARGIN <= currentObstacle.positionX and verifiedObstacle.positionX + 2*self.SAFE_MARGIN >= currentObstacle.positionX):
                    if currentObstacle.positionX <= verifiedObstacle.positionX and currentObstacle.positionY < verifiedObstacle.positionY:
                        if currentObstacle.positionY > collisionUpperLeftCorner.positionY:
                            collisionUpperLeftCorner = currentObstacle
                    if currentObstacle.positionX >= verifiedObstacle.positionX and currentObstacle.positionY < verifiedObstacle.positionY:
                        if currentObstacle.positionY > collisionUpperRightCorner.positionY:
                            collisionUpperRightCorner = currentObstacle
                    if currentObstacle.positionX <= verifiedObstacle.positionX and currentObstacle.positionY > verifiedObstacle.positionY:
                        if currentObstacle.positionY < collisionBottomLeftCorner.positionY:
                            collisionBottomLeftCorner = currentObstacle
                    if currentObstacle.positionX >= verifiedObstacle.positionX and currentObstacle.positionY > verifiedObstacle.positionY:
                        if currentObstacle.positionY < collisionBottomRightCorner.positionY:
                            collisionBottomRightCorner = currentObstacle
        return collisionUpperLeftCorner, collisionUpperRightCorner, collisionBottomLeftCorner, collisionBottomRightCorner




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
        for compteur in range (0, self.obstaclesList.__len__()):
            currentObstacle = self.obstaclesList[(compteur)]
            cv2.rectangle(img, (currentObstacle.positionX - self.SAFE_MARGIN, currentObstacle.positionY - self.SAFE_MARGIN), (currentObstacle.positionX + self.SAFE_MARGIN, currentObstacle.positionY + self.SAFE_MARGIN),
                      (0, 255, 0), -1, 1)
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
listObs.append(Obstacle((200,200)))
listObs.append(Obstacle((240,300)))
listObs.append(Obstacle((250,100)))
listObs.append(Obstacle((280,220)))
listObs.append(Obstacle((300,400)))
listObs.append(Obstacle((330,100)))

#listObs.append(Obstacle((220,400)))

listObs.append(Obstacle((700,350)))
#listObs.append(Obstacle((210,500)))


bob = GraphGenerator (listObs)
bob.generateGraph()
