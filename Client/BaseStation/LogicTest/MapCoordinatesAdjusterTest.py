from unittest import TestCase
from mock import MagicMock

from Client.BaseStation.Logic.MapCoordinatesAjuster import MapCoordinatesAjuster

class MapCoordinatesAdjusterTest(TestCase):

    def setUp(self):
        self.map = MagicMock()
        self.limit = MagicMock()
        self.limit.getMinCorner.return_value = (100,100)
        self.map.getMapLimit.return_value = self.limit
        self.mapCoordinatesAdjuster = MapCoordinatesAjuster(self.map)

    def test_goodConversion(self):
        convertedPoint = self.mapCoordinatesAdjuster.convertPoint((200,300))
        self.assertEqual(convertedPoint[0], 100)
        self.assertEqual(convertedPoint[1], 200)