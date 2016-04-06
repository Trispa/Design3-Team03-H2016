from unittest import TestCase

from Client.BaseStation.Logic.Pathfinding.Graph.Node import Node


class NodeTest(TestCase):

    def setUp(self):
        self.node2 = Node((200,200))
        self.node = Node((100,110))


    def test_initalisingGoodData(self):
        self.assertEqual(self.node.positionX, 100)
        self.assertEqual(self.node.positionY, 110)

    def test_setConnectedNode(self):
        self.node.addConnectedNode(self.node2)
        self.assertTrue(self.node.connectedNodes.__contains__(self.node2))

    def test_getConnectedNode(self):
        self.assertEqual(self.node.connectedNodes, self.node.getConnectedNodesList())