from unittest import TestCase
from mock import MagicMock
from mock import patch
import numpy as np
from Client.BaseStation.Logic.Pathfinding.MapAdaptator import MapAdaptator
from Client.BaseStation.Logic.Pathfinding.Obstacle import Obstacle


class MapAdaptatorTest(TestCase):

    def setUp(self):
        self.map = MagicMock()
        self.limit = MagicMock()
        self.limit.getMinCorner.return_value = (100,100)
        self.limit.getMaxCorner.return_value = (1000,900)
        self.map.getMapLimit.return_value = self.limit

        blueSquare = MagicMock()
        blueSquare.findCenterOfMass.return_value = 200,200
        obstacleList = [blueSquare]
        self.map.getShapesList.return_value = obstacleList

        self.mapAdaptator = MapAdaptator(self.map)


    def test_whenGetMapInfoIsCalledThenReturnGoodValues(self):
        goodmapSizeX, goodmapSizeY = 900, 800
        goodMinCorner = (100,100)
        goodObstacle = Obstacle((100,100))
        obstaclesList, mapSizeX, mapSizeY, minCorner = self.mapAdaptator.getMapInfo()

        self.assertEqual(goodmapSizeX, mapSizeX)
        self.assertEqual(goodmapSizeY, mapSizeY)
        self.assertEqual(goodMinCorner, minCorner)

        self.assertEqual(goodObstacle.positionX, obstaclesList[0].positionX)
        self.assertEqual(goodObstacle.positionY, obstaclesList[0].positionY)
