from unittest import TestCase
from mock import MagicMock
from mock import patch

from Client.BaseStation.Logic.Pathfinding.Path import  Path
from Client.BaseStation.Logic.Pathfinding.Graph.Node import Node

class PathTest(TestCase):

    def setUp(self):
        self.path = Path()
        self.path.append(Node((0,100)))
        self.path.append(Node((0,0)))


    def test_whenAdjustDistanceIsCalledThenDistanceIsUpdated(self):
        self.path.ajustDistance()
        goodDistance = 100

        self.assertEqual(goodDistance, self.path.totalDistance)


    def test_whenIsOpenIsCalledThenReturnGoodValue(self):
        theValue = self.path.isOpen()
        isOpen = False

        self.assertEqual(theValue,isOpen)


    def test_whenCloneIsCalledThenCopyIsEqual(self):
        pathClone = self.path.clone()
        for compteur in range(0, self.path.__len__()):
            self.assertTrue(pathClone.contains(self.path.nodeList[0]))
