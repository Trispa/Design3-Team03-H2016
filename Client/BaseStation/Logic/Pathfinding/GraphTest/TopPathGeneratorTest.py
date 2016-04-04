from unittest import TestCase
from mock import MagicMock
from Client.BaseStation.Logic.Pathfinding.Obstacle import Obstacle
from Client.BaseStation.Logic.Pathfinding.Graph.Node import Node
from Client.BaseStation.Logic.Pathfinding.Graph.TopPathGenerator import TopPathGenerator
from Client.BaseStation.Logic.Pathfinding.Graph.CollisionDetector import CollisionDetector

class TopPathGeneratorTest(TestCase):

    def setUp(self):
        self.collisionDetector = CollisionDetector(1000, 600, 90, [Obstacle((400,400))])

        self.graph = MagicMock()
        self.topPathGenerator = TopPathGenerator(90, 600, self.graph, self.collisionDetector)



    def test_whenWallIsTheNextObstacle(self):
        collisionUpperLeftCorner = Obstacle((100,0))
        collisionUpperRightCorner = Obstacle((280,0))
        currentObstacle = Obstacle((190,290))
        borderNodeLeftTop = Node((100,100))
        topLeftCorner = (100,200)
        borderNodeRightTop = Node((280,100))
        self.topPathGenerator.generateTopPath(collisionUpperLeftCorner, collisionUpperRightCorner, currentObstacle, borderNodeLeftTop, topLeftCorner, borderNodeRightTop)
        assert self.graph.connectTwoNodes.called

    def test_whenLeftObstacleIsTheImportantOne(self):
        collisionUpperLeftCorner = Obstacle((100,50))
        collisionUpperRightCorner = Obstacle((280,0))
        currentObstacle = Obstacle((190,290))
        borderNodeLeftTop = Node((100,100))
        topLeftCorner = (100,200)
        borderNodeRightTop = Node((280,100))
        self.topPathGenerator.generateTopPath(collisionUpperLeftCorner, collisionUpperRightCorner, currentObstacle, borderNodeLeftTop, topLeftCorner, borderNodeRightTop)
        assert self.graph.connectTwoNodes.called

    def test_whenRightObstacleIsTheImportantOne(self):
        collisionUpperLeftCorner = Obstacle((100,0))
        collisionUpperRightCorner = Obstacle((280,70))
        currentObstacle = Obstacle((190,290))
        borderNodeLeftTop = Node((100,100))
        topLeftCorner = (100,200)
        borderNodeRightTop = Node((280,100))
        self.topPathGenerator.generateTopPath(collisionUpperLeftCorner, collisionUpperRightCorner, currentObstacle, borderNodeLeftTop, topLeftCorner, borderNodeRightTop)
        assert self.graph.connectTwoNodes.called


