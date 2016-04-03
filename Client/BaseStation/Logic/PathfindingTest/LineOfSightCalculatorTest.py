from unittest import TestCase
from mock import MagicMock
from Client.BaseStation.Logic.Pathfinding.LineOfSightCalculator import LineOfSightCalculator

class LineOfSightCalculatorTest(TestCase):

    def setUp(self):
        self.goodPaths = []
        self.graph = MagicMock()
        self.lineOfSightCalculator = LineOfSightCalculator(self.graph)

    def test_test(self):
        self.lineOfSightCalculator.tryStraightLine(self.goodPaths)
        self.assertTrue(True)