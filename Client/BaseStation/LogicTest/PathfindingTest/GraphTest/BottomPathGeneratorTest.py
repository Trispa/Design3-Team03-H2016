from unittest import TestCase
from mock import MagicMock
from Client.BaseStation.Logic.Pathfinding.Obstacle import Obstacle
from Client.BaseStation.Logic.Pathfinding.Graph.Node import Node
from Client.BaseStation.Logic.Pathfinding.Graph.BottomPathGenerator import BottomPathGenerator
from Client.BaseStation.Logic.Pathfinding.Graph.CollisionDetector import CollisionDetector

class BottomPathGeneratorTest(TestCase):

    def setUp(self):
        self.collisionDetector = CollisionDetector(1000, 600, 90, [Obstacle((400,400))])

        self.graph = MagicMock()
        self.bottomPathGenerator = BottomPathGenerator(90, 600, self.graph, self.collisionDetector)



    def test_whenWallIsTheNextObstacle(self):
        collisionBottomLeftCorner = Obstacle((100,600))
        collisionBottomRightCorner = Obstacle((280,600))
        currentObstacle = Obstacle((190,290))
        borderNodeLeftTop = Node((100,400))
        topLeftCorner = (100,380)
        borderNodeRightTop = Node((280,400))
        self.bottomPathGenerator.generateBottomPath(collisionBottomLeftCorner, collisionBottomRightCorner, currentObstacle, borderNodeLeftTop, topLeftCorner, borderNodeRightTop)
        assert self.graph.connectTwoNodes.called

    def test_whenLeftObstacleIsTheImportantOne(self):
        collisionBottomLeftCorner = Obstacle((100,540))
        collisionBottomRightCorner = Obstacle((280,600))
        currentObstacle = Obstacle((190,290))
        borderNodeLeftTop = Node((100,400))
        topLeftCorner = (100,380)
        borderNodeRightTop = Node((280,400))
        self.bottomPathGenerator.generateBottomPath(collisionBottomLeftCorner, collisionBottomRightCorner, currentObstacle, borderNodeLeftTop, topLeftCorner, borderNodeRightTop)
        assert self.graph.connectTwoNodes.called


    def test_whenRightObstacleIsTheImportantOne(self):
        collisionBottomLeftCorner = Obstacle((100,600))
        collisionBottomRightCorner = Obstacle((280,500))
        currentObstacle = Obstacle((190,290))
        borderNodeLeftTop = Node((100,400))
        topLeftCorner = (100,380)
        borderNodeRightTop = Node((280,400))
        self.bottomPathGenerator.generateBottomPath(collisionBottomLeftCorner, collisionBottomRightCorner, currentObstacle, borderNodeLeftTop, topLeftCorner, borderNodeRightTop)
        assert self.graph.connectTwoNodes.called



