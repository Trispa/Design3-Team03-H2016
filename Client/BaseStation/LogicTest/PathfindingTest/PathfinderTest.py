from unittest import TestCase
from mock import MagicMock
from mock import patch
from Client.BaseStation.Logic.Pathfinding.Pathfinder import Pathfinder
from Client.BaseStation.Logic.Pathfinding.Obstacle import Obstacle

class PathfindingTest(TestCase):


    def setUp(self):
        self.map = MagicMock()
        self.limit = MagicMock()
        self.limit.getMinCorner.return_value = (100,100)
        self.limit.getMaxCorner.return_value = (1000,900)
        self.map.getMapLimit.return_value = self.limit

        blueSquare = MagicMock()
        blueSquare.findCenterOfMass.return_value = 370,370
        redSquare = MagicMock()
        redSquare.findCenterOfMass.return_value = 400,400
        obstacleList = [blueSquare, redSquare]

        self.map.getShapesList.return_value = obstacleList
        self.pathfinder = Pathfinder(self.map)

    def test_whenFindPathIsCalledThenReturnedPathIsNotGoingThroughtAnObstacle(self):
        goodpath = self.pathfinder.findPath((80,80), (500,500))
        self.assertTrue(goodpath.__len__() > 2)

    def test_whenFindPathIsCalledThenReturnedPathIsTheShortest(self):
        goodpath = self.pathfinder.findPath((80,80), (500,500))
        for compteur in range(0, self.pathfinder.goodPaths.__len__()):
            self.assertTrue(goodpath.totalDistance <= self.pathfinder.goodPaths[compteur].totalDistance)