from unittest import TestCase

from Client.BaseStation.Logic.Pathfinding.Graph.Graph import Graph
from Client.BaseStation.Logic.Pathfinding.Obstacle import Obstacle
from Client.BaseStation.Logic.Pathfinding.Graph.Node import Node


class GraphTest(TestCase):
    def setUp(self):
        obstacleList = [Obstacle((100,100)), Obstacle((300,200))]
        self.graph = Graph(obstacleList, 90)
        self.A_NODE1 = Node((200,300))
        self.A_NODE2 = Node((400,600))

        self.graph.generateSafeZone((0,100), (0,0), (100,0))

    def test_connectedNodesArePresentInNodesList(self):
        self.graph.connectTwoNodes(self.A_NODE1, self.A_NODE2)
        self.assertTrue(self.graph.nodesList.__contains__(self.A_NODE1))
        self.assertTrue(self.graph.nodesList.__contains__(self.A_NODE2))

    def test_findGoodSafeZone(self):
        safeNode = self.graph.findGoodSafeNodeToGo((40,50))
        goodSafeNode = Node((50,50))
        self.assertEqual(safeNode.positionY, goodSafeNode.positionY)
        self.assertEqual(safeNode.positionX, goodSafeNode.positionX)