from Client.BaseStation.Logic.Pathfinding.Graph.GraphGenerator import GraphGenerator
from Client.BaseStation.Logic.Pathfinding.Path import Path
from Client.BaseStation.Logic.Pathfinding.MapAdaptator import MapAdaptator
from Client.BaseStation.Logic.Pathfinding.Graph.Node import Node
from Client.BaseStation.Logic.Pathfinding.LineOfSightCalculator import LineOfSightCalculator
import cv2
import numpy as np

class Pathfinder:
    def __init__(self, map):
        self.mapAdaptator = MapAdaptator(map)
        obstaclesList, mapSizeX, mapSizeY, minCorner = self.mapAdaptator.getMapInfo()
        self.minCorner = minCorner
        self.graphGenerator = GraphGenerator(obstaclesList, mapSizeX, mapSizeY)
        self.graph = self.graphGenerator.generateGraph()
        self.lineOfSightCalculator = LineOfSightCalculator(self.graph)
        self.pathsList = []
        self.goodPaths = []
        self.indice = 0
        self.theGoodPath = Path()


    def findPath(self, positionRobot, pointToMoveTo):
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        startingPathNode = self.graph.findGoodSafeNodeToGo(positionRobot)
        endingPathNode = self.graph.findGoodSafeNodeToGo(pointToMoveTo)

        path = Path()
        path.append(Node(positionRobot))
        path.append(startingPathNode)
        self.pathsList.append(path)
        self.__findAllPaths(path, endingPathNode)

        goodPath = Path()
        goodPath.append(Node((0,0)))
        goodPath.totalDistance = 99999
        for compteur in range(0, self.goodPaths.__len__()):
            currentPath = self.goodPaths[compteur]
            currentPath.append(Node(pointToMoveTo))

        self.__polishGoodPaths()
        self.lineOfSightCalculator.tryStraightLine(self.goodPaths)

        for compteur in range(0, self.goodPaths.__len__()):
            currentPath= self.goodPaths[compteur]
            currentPath.ajustDistance()
            if currentPath.totalDistance < goodPath.totalDistance:
                    goodPath = currentPath
        self.printPath(goodPath)
        self.theGoodPath = goodPath
        #self.__displayPathfinder(goodPath, positionRobot)
        return goodPath


    def __polishGoodPaths(self):
        for compteur in range(0,self.goodPaths.__len__()):
            path = self.goodPaths[compteur]
            nodesToBeRemoved = []

            for compteur in range(1, path.__len__()):
                if path[compteur].isASafeNode == True:
                    previousNode = path[compteur-1]
                    nextNode = path[compteur+1]

                    if previousNode.positionX != nextNode.positionX:
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


    def drawPath(self, img):
        for compteur in range (1, self.theGoodPath.__len__()):
            startLine = (self.theGoodPath[compteur-1].positionX + self.minCorner[0], self.theGoodPath[compteur-1].positionY + self.minCorner[1])
            endLine =  (self.theGoodPath[compteur].positionX + self.minCorner[0], self.theGoodPath[compteur].positionY + self.minCorner[1])
            cv2.line(img, startLine, endLine,
                      (0, 0, 255), 2, 1)


    #methode pour afficher le path dans console, pas importante
    def printPath(self, goodPath):
        for compteur in range(0, goodPath.__len__()):
            print "path:", goodPath[compteur].positionX, goodPath[compteur].positionY
        print goodPath.totalDistance

    #methode pour display les shits du pathfinding, pas importante non plus
    def __displayPathfinder(self, goodPath, positionRobot):
        img = np.zeros((600, 1000, 3), np.uint8)

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
        cv2.imwrite('image' + str(self.indice) + '.jpg', img)
        self.indice = self.indice + 1




