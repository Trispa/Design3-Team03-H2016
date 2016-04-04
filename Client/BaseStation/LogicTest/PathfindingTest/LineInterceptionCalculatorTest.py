from unittest import TestCase

from Client.BaseStation.Logic.Pathfinding.LineInterceptionCalculator import LineInterceptionCalculator

class LineInterceptionCalculatorTest(TestCase):

    def setUp(self):
        self.lineCalculator = LineInterceptionCalculator()

    def test_twoLineWithoutIntersection(self):
        intersection = self.lineCalculator.findInterception((0,0), (100,0), (100,100), (200,100))
        self.assertEqual(intersection, False)

    def test_twoLineWithIntersection(self):
        intersection = self.lineCalculator.findInterception((0,0), (-10,-10), (0,0), (-10,10))
        theTrueIntersection = (0,0)
        self.assertEqual(intersection[0], theTrueIntersection[0])
        self.assertEqual(intersection[1], theTrueIntersection[1])