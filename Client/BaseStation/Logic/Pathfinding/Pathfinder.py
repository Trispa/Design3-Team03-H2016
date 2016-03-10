from Client.BaseStation.Logic.Pathfinding.Graph.GraphGenerator import GraphGenerator
from Client.BaseStation.Logic.Pathfinding.Path import Path
from Client.BaseStation.Logic.Pathfinding.Obstacle import Obstacle
from Client.BaseStation.Logic.Pathfinding.Graph.Node import Node
import cv2
import numpy as np

class Pathfinder:
    def __init__(self, obstaclesList):
        self.graphGenerator = GraphGenerator(obstaclesList)
        self.graph = self.graphGenerator.generateGraph()
        self.pathsList = []



    def findPath(self, positionRobot, pointToMoveTo):
        startingPathNode = self.graphGenerator.findClosestNodeTo(positionRobot)
        endingPathNode = self.graphGenerator.findClosestNodeTo(pointToMoveTo)
        print "ending:", endingPathNode.positionX, endingPathNode.positionY
        path = Path()
        path.append(startingPathNode)
        self.pathsList.append(path)
        self.__findAllPaths(path, endingPathNode)
        goodPath = Path()
        goodPath.totalDistance = 99999
        for compteur in range(0, self.pathsList.__len__()):
            print "path compteur:", compteur
            currentPath = self.pathsList[compteur]

            if currentPath[currentPath.__len__()-1] == endingPathNode:
                print "endingPathNode:", currentPath[currentPath.__len__()-1].positionX, currentPath[currentPath.__len__()-1].positionY
                currentPath = self.pathsList[compteur]
                if currentPath.totalDistance < goodPath.totalDistance:
                    print currentPath.totalDistance, " < ", goodPath.totalDistance
                    goodPath = currentPath
        goodPath.append(Node(pointToMoveTo))
        #return goodPath
        self.__displayPathfinder(goodPath, positionRobot)

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
        couleur = 0
        for compteur in range (0, self.graphGenerator.obstaclesList.__len__()):
            currentObstacle = self.graphGenerator.obstaclesList[(compteur)]
            cv2.rectangle(img, (currentObstacle.positionX - self.graphGenerator.SAFE_MARGIN, currentObstacle.positionY - self.graphGenerator.SAFE_MARGIN), (currentObstacle.positionX + self.graphGenerator.SAFE_MARGIN, currentObstacle.positionY + self.graphGenerator.SAFE_MARGIN),
                      (0, 255, 0), -1, 1)
            self.graphGenerator.nodesList.sort(key=lambda node: node.positionX)
        for compteur in range (0, self.graphGenerator.nodesList.__len__()):

            currentNode = self.graphGenerator.nodesList[(compteur)]
            departPoint = (currentNode.positionX, currentNode.positionY)
            connectedNode = currentNode.getConnectedNodesList()
            print "\nnode:", currentNode.positionX, currentNode.positionY
            for compteurConnected in range(0, connectedNode.__len__()):
                finalNode = connectedNode[(compteurConnected)]
                finalPoint = (finalNode.positionX, finalNode.positionY)
                print "connected with:", finalNode.positionX, finalNode.positionY
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


listObs = []
#listObs.append(Obstacle((180,200)))
#listObs.append(Obstacle((220,300)))
listObs.append(Obstacle((230,301)))
listObs.append(Obstacle((290,420)))
#listObs.append(Obstacle((340,400)))
listObs.append(Obstacle((320,300)))
listObs.append(Obstacle((265,150)))
#listObs.append(Obstacle((215,400)))

#listObs.append(Obstacle((700,350)))
#listObs.append(Obstacle((190,500)))
#listObs.append(Obstacle((210,300)))
#listObs.append(Obstacle((200,520)))
#listObs.append(Obstacle((220,450)))
#listObs.append(Obstacle((203,380)))
#listObs.append(Obstacle((207,300)))
#listObs.append(Obstacle((210,200)))
bob = Pathfinder(listObs)
bob.findPath((700,100),(500,500))





