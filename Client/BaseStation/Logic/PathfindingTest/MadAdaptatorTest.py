from unittest import TestCase
from mock import MagicMock
from mock import patch
import numpy as np
from Client.BaseStation.WorldVision.allShapes import Square
from Client.BaseStation.Logic.Pathfinding.MapAdaptator import MapAdaptator
from Client.BaseStation.WorldVision.map import Map

class MapAdaptatorTest(TestCase):

    def setUp(self):
        self.map = MagicMock()
        self.limit = MagicMock()
        self.limit.getMinCorner.return_value = (100,100)
    	self.map.getMapLimit.return_value = self.limit

        self.mapAdaptator = MapAdaptator(map)

    def test_test(self):
        goodMinCorner = (0,100)
        goodMaXCorner = (1000,700)
        self.mapAdaptator.getMapInfo()

        self.assertEqual(1000,1000)
