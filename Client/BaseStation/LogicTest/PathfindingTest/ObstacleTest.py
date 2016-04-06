from unittest import TestCase


from Client.BaseStation.Logic.Pathfinding.Obstacle import Obstacle
from Client.BaseStation.Logic.Pathfinding.Graph.Node import Node


class ObstacleTest(TestCase):
    A_POINT = (100,200)
    A_NODE = Node((200,100))

    def setUp(self):
        self.obstacle = Obstacle(self.A_POINT)

    def test_whenInitialiseThenGoodDataAreSet(self):
        self.assertEqual(self.obstacle.positionX, self.A_POINT[0])
        self.assertEqual(self.obstacle.positionY, self.A_POINT[1])

    def test_setStartingNode(self):
        self.obstacle.setStartingNode(self.A_NODE)
        self.assertEqual(self.obstacle.startingNode, self.A_NODE)