from unittest import TestCase
from mock import MagicMock

from Client.BaseStation.Logic.Pathfinding.Graph.EndNodeGenerator import EndNodeGenerator
from Client.BaseStation.Logic.Pathfinding.Graph.CollisionDetector import CollisionDetector
from Client.BaseStation.Logic.Pathfinding.Obstacle import Obstacle

class EndNodeGeneratorTest(TestCase):

    def setUp(self):
        self.obstaclesList = [Obstacle((60,150)), Obstacle((90,500)), Obstacle((200,100)), Obstacle((230,300)), Obstacle((320, 150))]
        self.collisionDetector = CollisionDetector(1000, 600, 50, self.obstaclesList)
        self.graph = MagicMock()

        self.EndNodeGenerator = EndNodeGenerator(1000, 600, 50, self.obstaclesList, self.collisionDetector, self.graph)
        self.EndNodeGenerator.generateEndNode(self.obstaclesList[0],(110,10),(110,110),self.obstaclesList[1], Obstacle((110,0)), 0)

    def test_whenEndNodeIsCalledThenGenerateSafeZoneIsNotCalledToo(self):
        self.assertTrue(self.graph.generateSafeZone.call_count != 0)