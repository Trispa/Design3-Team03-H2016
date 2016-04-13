from Client.BaseStation.Logic.Pathfinding.Graph.CollisionDetector import CollisionDetector
from Client.BaseStation.Logic.Pathfinding.Graph.EndNodeGenerator import EndNodeGenerator
from Client.BaseStation.Logic.Pathfinding.Graph.Node import Node
from Client.BaseStation.Logic.Pathfinding.Graph.BottomPathGenerator import BottomPathGenerator
from Client.BaseStation.Logic.Pathfinding.Graph.TopPathGenerator import TopPathGenerator
from Client.BaseStation.Logic.Pathfinding.Graph.Graph import Graph

class GraphGenerator:
    SAFE_MARGIN = 85


    def __init__(self, obstaclesList, mapSizeX, mapSizeY):
        self.MAP_SIZE_X = mapSizeX
        self.MAP_SIZE_Y = mapSizeY
        self.graph = Graph(obstaclesList, self.SAFE_MARGIN)
        self.collisionDetector = CollisionDetector(self.MAP_SIZE_X, self.MAP_SIZE_Y, self.SAFE_MARGIN, obstaclesList)
        self.endNodeGenerator = EndNodeGenerator(self.MAP_SIZE_X, self.MAP_SIZE_Y, self.SAFE_MARGIN, obstaclesList,
                                                 self.collisionDetector, self.graph)
        self.bottomPathGenerator = BottomPathGenerator(self.SAFE_MARGIN, mapSizeY, self.graph, self.collisionDetector)
        self.topPathGenerator = TopPathGenerator(self.SAFE_MARGIN, mapSizeY, self.graph, self.collisionDetector)
        self.obstaclesList = obstaclesList
        self.obstaclesList.sort(key=lambda obstacle: obstacle.positionX)



    def generateGraph(self):
        firstObstacle = self.obstaclesList[0]
        if self.collisionDetector.isCollidingWithWallFront(firstObstacle) == False:
            self.__defaultStart(firstObstacle)

        for compteur in range(0, self.obstaclesList.__len__()):
            currentObstacle = self.obstaclesList[(compteur)]
            startingNode = currentObstacle.startingNode
            if compteur < self.obstaclesList.__len__() - 1:
                nextObstacle = self.obstaclesList[compteur + 1]
                if nextObstacle.startingNode.positionX == 0:
                    nextObstacle.setStartingNode(currentObstacle.startingNode)

            currentOstacleTopLeftCorner = (currentObstacle.positionX - self.SAFE_MARGIN, currentObstacle.positionY - self.SAFE_MARGIN)
            currentOstacleTopRightCorner = (currentObstacle.positionX + self.SAFE_MARGIN, currentObstacle.positionY - self.SAFE_MARGIN)
            currentOstacleBottomRightCorner = (currentObstacle.positionX + self.SAFE_MARGIN, currentObstacle.positionY + self.SAFE_MARGIN)
            currentOstacleBottomLeftCorner = (currentObstacle.positionX - self.SAFE_MARGIN, currentObstacle.positionY + self.SAFE_MARGIN)

            collisionUpperLeftCorner, collisionUpperRightCorner, collisionBottomLeftCorner, collisionBottomRightCorner = self.collisionDetector.detectCloserObstacleForEachCornerXAxis(currentObstacle)

            borderNodeLeftTop = Node(
                (currentOstacleTopLeftCorner[0], (currentOstacleTopLeftCorner[1] + collisionUpperLeftCorner.positionY + self.SAFE_MARGIN) / 2))

            borderNodeRightTop = Node(
                (currentOstacleTopRightCorner[0], (currentOstacleTopRightCorner[1] + collisionUpperRightCorner.positionY + self.SAFE_MARGIN) / 2))

            borderNodeLeftBottom = Node((currentOstacleBottomLeftCorner[0],
                (currentOstacleBottomLeftCorner[1] + collisionBottomLeftCorner.positionY - self.SAFE_MARGIN) / 2))

            borderNodeRightBottom = Node((currentOstacleBottomRightCorner[0],
                (currentOstacleBottomRightCorner[1] + collisionBottomRightCorner.positionY - self.SAFE_MARGIN) / 2))

            resultTop, collisionInnerTop = self.collisionDetector.hasUpperInnerCollision(currentObstacle)
            resultBot, collisionInnerBot = self.collisionDetector.hasLowerInnerCollision(currentObstacle)
            if not(self.collisionDetector.hasEndInnerCollision(currentObstacle) and (resultTop and collisionInnerTop[-1].positionY > currentObstacle.positionY) and (resultBot and collisionInnerBot[-1].positionY > currentObstacle.positionY)):
                endNode = self.endNodeGenerator.generateEndNode(currentObstacle, currentOstacleTopRightCorner, currentOstacleBottomRightCorner,
                                                            collisionBottomRightCorner, collisionUpperRightCorner, compteur)
            else:
                #Might be the Problem
                endNode = Node((1000,1000))

            if self.collisionDetector.isCollidingWithWallFront(currentObstacle) == False:
                self.__generateFrontPath(borderNodeLeftBottom, borderNodeLeftTop, currentObstacle, startingNode)

            if self.collisionDetector.isCollidingWithWallUpper(currentObstacle) == False:
                self.topPathGenerator.generateTopPath(collisionUpperLeftCorner, collisionUpperRightCorner,
                                   currentObstacle, borderNodeLeftTop, currentOstacleTopLeftCorner, borderNodeRightTop)

            if self.collisionDetector.isCollidingWithWallLower(currentObstacle) == False:
                self.bottomPathGenerator.generateBottomPath(collisionBottomLeftCorner, collisionBottomRightCorner, currentObstacle,
                                                            borderNodeLeftBottom, currentOstacleBottomLeftCorner, borderNodeRightBottom)

            if self.collisionDetector.isCollidingWithWallBack(currentObstacle) == False:
                self.__generateEndPath(borderNodeRightBottom, borderNodeRightTop, currentObstacle, endNode)

        return self.graph


    def __generateEndPath(self, borderNodeRightBottom, borderNodeRightTop, currentObstacle, endNode):
        if self.collisionDetector.hasEndInnerCollision(currentObstacle) == False:
            if self.collisionDetector.isCollidingWithWallUpper(currentObstacle) == False:
                self.graph.connectTwoNodes(borderNodeRightTop, endNode)

            if self.collisionDetector.isCollidingWithWallLower(currentObstacle) == False:
                self.graph.connectTwoNodes(borderNodeRightBottom, endNode)
        else:
            result, collidingObstacle = self.collisionDetector.hasLowerInnerCollision(currentObstacle)
            if result == False or collidingObstacle[-1].positionX < currentObstacle.positionX:
                if self.collisionDetector.isCollidingWithWallLower(currentObstacle) == False:
                    self.graph.connectTwoNodes(borderNodeRightBottom, endNode)

            result, collidingObstacle = self.collisionDetector.hasUpperInnerCollision(currentObstacle)
            if result == False or collidingObstacle[-1].positionX < currentObstacle.positionX:
                if self.collisionDetector.isCollidingWithWallUpper(currentObstacle) == False:
                    self.graph.connectTwoNodes(borderNodeRightTop, endNode)


    def __generateFrontPath(self, borderNodeLeftBottom, borderNodeLeftTop, currentObstacle, startingNode):
        if self.collisionDetector.hasFrontalInnerCollision(currentObstacle) == False:
            if self.collisionDetector.isCollidingWithWallLower(currentObstacle) == False:
                self.graph.connectTwoNodes(startingNode, borderNodeLeftBottom)

            if self.collisionDetector.isCollidingWithWallUpper(currentObstacle) == False:
                self.graph.connectTwoNodes(startingNode, borderNodeLeftTop)
        else:
            result, collidingObstacle = self.collisionDetector.hasUpperInnerCollision(currentObstacle)

            if result == False or collidingObstacle[0].positionX > currentObstacle.positionX:
                if self.collisionDetector.isCollidingWithWallUpper(currentObstacle) == False:
                    self.graph.connectTwoNodes(startingNode, borderNodeLeftTop)

            result, collidingObstacle = self.collisionDetector.hasLowerInnerCollision(currentObstacle)
            if result == False or collidingObstacle[0].positionX > currentObstacle.positionX:
                if self.collisionDetector.isCollidingWithWallLower(currentObstacle) == False:
                    self.graph.connectTwoNodes(startingNode, borderNodeLeftBottom)


    def __defaultStart(self, firstObstacle):
        safeZoneCornerTopLeft = (0, 0 + (self.SAFE_MARGIN -20))
        safeZoneCornerBotLeft = (0, self.MAP_SIZE_Y - (self.SAFE_MARGIN-20))
        safeZoneCornerTopRight = (firstObstacle.positionX - self.SAFE_MARGIN, safeZoneCornerTopLeft[1])
        startingNode = self.graph.generateSafeZone(safeZoneCornerBotLeft, safeZoneCornerTopLeft, safeZoneCornerTopRight)
        firstObstacle.setStartingNode(startingNode)
