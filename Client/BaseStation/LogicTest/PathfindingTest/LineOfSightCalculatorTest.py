from unittest import TestCase
from mock import MagicMock
from Client.BaseStation.Logic.Pathfinding.LineOfSightCalculator import LineOfSightCalculator
from Client.BaseStation.Logic.Pathfinding.Path import Path
from Client.BaseStation.Logic.Pathfinding.Graph.Node import Node

class LineOfSightCalculatorTest(TestCase):

    def setUp(self):
        self.noLineOfSightPath = Path()
        self.lineOfSightPath = Path()
        self.noLineOfSightPath.nodeList = [Node((100, 100)), Node((200, 100))]
        self.lineOfSightPath.nodeList = [Node((0, 0)), Node((50, 50)), Node((50, 0))]
        self.goodPaths = []
        self.graph = MagicMock()
        self.lineOfSightCalculator = LineOfSightCalculator(self.graph)


    def test_whenPathHasNoLineOfSightThenPathStayTheSame(self):
        self.goodPaths.append(self.noLineOfSightPath)
        goodLenght = self.noLineOfSightPath.__len__()
        self.lineOfSightCalculator.tryStraightLine(self.goodPaths)
        obtainedLenght = self.noLineOfSightPath.__len__()

        self.assertEqual(goodLenght,obtainedLenght)


    def test_whenPathHasLineOfSightThenPathStayTheSame(self):
        self.goodPaths.append(self.lineOfSightPath)
        self.lineOfSightCalculator.tryStraightLine(self.goodPaths)

        self.assertEqual(self.lineOfSightPath.contains(Node((50,50))),False)