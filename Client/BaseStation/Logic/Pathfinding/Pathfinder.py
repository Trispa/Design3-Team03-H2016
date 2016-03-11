from Client.BaseStation.Logic.Pathfinding.Graph.GraphGenerator import GraphGenerator
from Client.BaseStation.Logic.Pathfinding.Path import Path
from Client.BaseStation.Logic.Pathfinding.MapAdaptator import MapAdaptator
from Client.BaseStation.Logic.Pathfinding.Graph.Node import Node
import cv2
import numpy as np

class Pathfinder:
    def __init__(self, map):
        self.mapAdaptator = MapAdaptator(map)
        obstaclesList, mapSizeX, mapSizeY = self.mapAdaptator.getMapInfo()
        self.graphGenerator = GraphGenerator(obstaclesList, mapSizeX, mapSizeY)
        self.graph = self.graphGenerator.generateGraph()
        self.pathsList = []



    def findPath(self, positionRobot, pointToMoveTo):
        startingPathNode = self.graph.findClosestNodeTo(positionRobot)
        endingPathNode = self.graph.findClosestNodeTo(pointToMoveTo)
        path = Path()
        path.append(startingPathNode)
        self.pathsList.append(path)
        self.__findAllPaths(path, endingPathNode)
        goodPath = Path()
        goodPath.totalDistance = 99999
        for compteur in range(0, self.pathsList.__len__()):
            currentPath = self.pathsList[compteur]

            if currentPath[currentPath.__len__()-1] == endingPathNode:

                currentPath = self.pathsList[compteur]
                if currentPath.totalDistance < goodPath.totalDistance:

                    goodPath = currentPath
        goodPath.append(Node(pointToMoveTo))
        print("find path")
        self.__displayPathfinder(goodPath, positionRobot)
        return goodPath


    def printPath(self, goodPath):
        for compteur in range(0, goodPath.__len__()):
            print "path:", goodPath[compteur].positionX, goodPath[compteur].positionY
        print goodPath.totalDistance

    def __findAllPaths(self, path, endingPathNode):
        lastNode = path[path.__len__()-1]

        if lastNode != endingPathNode and path.isOpen() == True:

            for compteur in range(0, lastNode.connectedNodes.__len__()):

                if (path.contains(lastNode.connectedNodes[compteur]) == False):

                    newPath = path.clone()
                    newPath.append(lastNode.connectedNodes[compteur])
                    self.pathsList.append(newPath)
                    self.__findAllPaths(newPath, endingPathNode)
            self.pathsList.remove(path)

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

            for compteurConnected in range(0, connectedNode.__len__()):
                finalNode = connectedNode[(compteurConnected)]
                finalPoint = (finalNode.positionX, finalNode.positionY)

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

        cv2.imshow('image', img)
        while (1):
            esc = cv2.waitKey(1)
            if esc == 27: #escape pressed
                break
        cv2.destroyAllWindows







