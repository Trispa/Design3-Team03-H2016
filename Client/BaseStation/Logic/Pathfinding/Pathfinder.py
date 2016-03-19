from Client.BaseStation.Logic.Pathfinding.Graph.GraphGenerator import GraphGenerator
from Client.BaseStation.Logic.Pathfinding.Path import Path
from Client.BaseStation.Logic.Pathfinding.MapAdaptator import MapAdaptator
from Client.BaseStation.Logic.Pathfinding.Obstacle import Obstacle
from Client.BaseStation.Logic.Pathfinding.Graph.Node import Node
from Client.BaseStation.Logic.Pathfinding.LineInterceptionCalculator import LineInterceptionCalculator
import cv2
import numpy as np

class Pathfinder:
    def __init__(self, obstaclesList): # (self,map)
        mapSizeX = 1000
        mapSizeY = 600
        #self.mapAdaptator = MapAdaptator(map)
        #obstaclesList, mapSizeX, mapSizeY = self.mapAdaptator.getMapInfo()
        self.graphGenerator = GraphGenerator(obstaclesList, mapSizeX, mapSizeY)
        self.graph = self.graphGenerator.generateGraph()
        self.lineInterceptionCalculator = LineInterceptionCalculator()
        self.pathsList = []
        self.goodPaths = []



    def findPath(self, positionRobot, pointToMoveTo):
        startingPathNode = self.graph.findGoodSafeNodeToGo(positionRobot)
        endingPathNode = self.graph.findGoodSafeNodeToGo(pointToMoveTo)

        path = Path()
        path.append(Node(positionRobot))
        path.append(startingPathNode)
        self.pathsList.append(path)
        self.__findAllPaths(path, endingPathNode)
        goodPath = Path()
        goodPath.totalDistance = 99999

        for compteur in range(0, self.goodPaths.__len__()):
            currentPath = self.goodPaths[compteur]
            currentPath.append(Node(pointToMoveTo))

        self.__polishGoodPaths()
        self.__tryStraightLine()

        for compteur in range(0, self.goodPaths.__len__()):
            currentPath= self.goodPaths[compteur]
            currentPath.ajustDistance()
            if currentPath.totalDistance < goodPath.totalDistance:
                    goodPath = currentPath
        self.printPath(goodPath)
        self.__displayPathfinder(goodPath, positionRobot)
        return goodPath


    def __tryStraightLine(self):
        for compteurPath in range(0, self.goodPaths.__len__()):
            currentPath = self.goodPaths[compteurPath]
            nodesToBeRemoved = []
            compteurNode = 0
            self.printPath(currentPath)
            while compteurNode < currentPath.__len__():
                currentNode = currentPath[compteurNode]
                compteurFinalNode = currentPath.__len__()-1
                lineOfSight = False
                while compteurFinalNode > compteurNode+1:
                    finalNode = currentPath[compteurFinalNode]
                    if lineOfSight == False:
                        topResult = True
                        botResult = True
                        leftResult = True
                        rightResult = True
                        for compteurObstacle in range(0, self.graph.obstaclesList.__len__()-1):
                            currentObstacle = self.graph.obstaclesList[compteurObstacle]
                            pointB1 = (currentObstacle.positionX-self.graph.SAFE_MARGIN, currentObstacle.positionY-self.graph.SAFE_MARGIN)
                            pointB2 = (currentObstacle.positionX+self.graph.SAFE_MARGIN, currentObstacle.positionY-self.graph.SAFE_MARGIN)

                            pointA1 = (currentNode.positionX, currentNode.positionY)
                            pointA2 = (finalNode.positionX, finalNode.positionY)
                            intersection = self.lineInterceptionCalculator.findInterception(pointA1, pointA2, pointB1, pointB2)

                            if intersection != False:
                                if (intersection[0] < pointB2[0] and intersection[0] > pointB1[0]) and (intersection[0] < pointA2[0] and intersection[0] > pointA1[0]):
                                    topResult = False

                            pointB1 = (currentObstacle.positionX-self.graph.SAFE_MARGIN, currentObstacle.positionY+self.graph.SAFE_MARGIN)
                            pointB2 = (currentObstacle.positionX+self.graph.SAFE_MARGIN, currentObstacle.positionY+self.graph.SAFE_MARGIN)
                            intersection = self.lineInterceptionCalculator.findInterception(pointA1, pointA2, pointB1, pointB2)
                            if intersection != False:
                                if (intersection[0] < pointB2[0] and intersection[0] > pointB1[0]) and (intersection[0] < pointA2[0] and intersection[0] > pointA1[0]):
                                    botResult = False

                            pointB1 = (currentObstacle.positionX-self.graph.SAFE_MARGIN, currentObstacle.positionY-self.graph.SAFE_MARGIN)
                            pointB2 = (currentObstacle.positionX-self.graph.SAFE_MARGIN, currentObstacle.positionY+self.graph.SAFE_MARGIN)
                            intersection = self.lineInterceptionCalculator.findInterception(pointA1, pointA2, pointB1, pointB2)
                            if intersection != False:
                                if (intersection[1] < pointB2[1] and intersection[1] > pointB1[1]) and (intersection[1] < pointA2[1] and intersection[1] > pointA1[1]):
                                    leftResult = False

                            pointB1 = (currentObstacle.positionX+self.graph.SAFE_MARGIN, currentObstacle.positionY-self.graph.SAFE_MARGIN)
                            pointB2 = (currentObstacle.positionX+self.graph.SAFE_MARGIN, currentObstacle.positionY+self.graph.SAFE_MARGIN)
                            intersection = self.lineInterceptionCalculator.findInterception(pointA1, pointA2, pointB1, pointB2)
                            if intersection != False:
                                if (intersection[1] < pointB2[1] and intersection[1] > pointB1[1]) and (intersection[1] < pointA2[1] and intersection[1] > pointA1[1]):
                                    rightResult = False

                        if topResult == True and botResult == True and leftResult == True and rightResult == True:
                            lineOfSight = True

                            for compteurRemoved in range(compteurNode+1, compteurFinalNode):
                                nodesToBeRemoved.append(currentPath[compteurRemoved])
                            compteurNode = compteurFinalNode -1
                    compteurFinalNode += -1
                compteurNode += 1

            for compteurToBeRemoved in range(0, nodesToBeRemoved.__len__()):
                currentPath.remove(nodesToBeRemoved[compteurToBeRemoved])






    def printPath(self, goodPath):
        for compteur in range(0, goodPath.__len__()):
            print "path:", goodPath[compteur].positionX, goodPath[compteur].positionY
        print goodPath.totalDistance

    def __polishGoodPaths(self):
        for compteur in range(0,self.goodPaths.__len__()):
            path = self.goodPaths[compteur]
            nodesToBeRemoved = []
            for compteur in range(0, path.__len__()):
                if path[compteur].isASafeNode == True:
                    try:
                        previousNode = path[compteur-1]
                        nextNode = path[compteur+1]
                        if previousNode.positionX != nextNode.positionX:
                            nodesToBeRemoved.append(path[compteur])
                    except IndexError:
                        nodesToBeRemoved.append(path[compteur])
            for compteur in range(0, nodesToBeRemoved.__len__()):
                path.remove(nodesToBeRemoved[compteur])

    def __findAllPaths(self, path, endingPathNode):
        lastNode = path[-1]
        if lastNode != endingPathNode and path.isOpen() == True:
            for compteur in range(0, lastNode.connectedNodes.__len__()):

                if (path.contains(lastNode.connectedNodes[compteur]) == False):

                    newPath = path.clone()
                    newPath.append(lastNode.connectedNodes[compteur])
                    self.pathsList.append(newPath)
                    self.__findAllPaths(newPath, endingPathNode)
            self.pathsList.remove(path)
        elif lastNode == endingPathNode:
            self.goodPaths.append(path)

    def __displayPathfinder(self, goodPath, positionRobot):
        img = np.zeros((600, 1000, 3), np.uint8)
        cv2.namedWindow('image')
        for compteur in range (0, self.graphGenerator.obstaclesList.__len__()):
            currentObstacle = self.graphGenerator.obstaclesList[(compteur)]
            cv2.rectangle(img, (currentObstacle.positionX - self.graphGenerator.SAFE_MARGIN, currentObstacle.positionY - self.graphGenerator.SAFE_MARGIN), (currentObstacle.positionX + self.graphGenerator.SAFE_MARGIN, currentObstacle.positionY + self.graphGenerator.SAFE_MARGIN),
                      (0, 255, 0), -1, 1)
            self.graph.nodesList.sort(key=lambda node: node.positionX)
        for compteur in range (0, self.graph.nodesList.__len__()):
            currentNode = self.graph.nodesList[(compteur)]
            departPoint = (currentNode.positionX, currentNode.positionY)
            connectedNode = currentNode.getConnectedNodesList()
            #print "GRAPh", currentNode.positionX, currentNode.positionY
            for compteurConnected in range(0, connectedNode.__len__()):
                finalNode = connectedNode[(compteurConnected)]
                finalPoint = (finalNode.positionX, finalNode.positionY)
                #print "     Connected", finalNode.positionX, finalNode.positionY
                cv2.line(img, departPoint, finalPoint,
                      (255, 0, 0), 2, 1)

        for compteur in range (0, goodPath.__len__()):
            if compteur == 0:
                startLine = positionRobot
            else:
                startLine = (goodPath[compteur-1].positionX,goodPath[compteur-1].positionY)
            endLine =  (goodPath[compteur].positionX,goodPath[compteur].positionY)
            cv2.line(img, startLine, endLine,
                      (0, 0, 255), 2, 1)
            
        for compteur in range (0, self.graph.safeZonesList.__len__()):
            currentZone = self.graph.safeZonesList[compteur]
            cv2.rectangle(img, currentZone.cornerTopLeft, currentZone.cornerBottomRight,
                      (0, 150, 150), 2, 1)
        cv2.imshow('image', img)
        while (1):
            esc = cv2.waitKey(1)
            if esc == 27: #escape pressed
                break
        cv2.destroyAllWindows

obstacleList = []
obstacleList.append(Obstacle((40,425)))
obstacleList.append(Obstacle((370,200)))
obstacleList.append(Obstacle((950,450)))
#obstacleList.append(Obstacle((360,440)))
#obstacleList.append(Obstacle((390,550)))
obstacleList.append(Obstacle((420,420)))
obstacleList.append(Obstacle((395,390)))
pathfinder = Pathfinder(obstacleList)
pathfinder.findPath((200,400), (520,300))




