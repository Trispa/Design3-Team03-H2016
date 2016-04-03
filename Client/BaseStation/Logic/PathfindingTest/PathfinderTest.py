from unittest import TestCase
from mock import MagicMock
from mock import patch
from Client.BaseStation.Logic.Pathfinding.Pathfinder import Pathfinder
from Client.BaseStation.Logic.Pathfinding.Obstacle import Obstacle

class PathfindingTest(TestCase):


    def setUp(self):
        self.map = MagicMock()
        self.map.obstaclesList.return_value = ([Obstacle((100,100))])
        self.pathfinder = Pathfinder(self.map)

    def test_whenInitializingPathfinderThenGoodData(self):
        self.assertTrue(True)