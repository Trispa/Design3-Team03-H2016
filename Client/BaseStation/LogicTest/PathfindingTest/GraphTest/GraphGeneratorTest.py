from unittest import TestCase
from mock import MagicMock

from Client.BaseStation.Logic.Pathfinding.Graph.GraphGenerator import GraphGenerator
from Client.BaseStation.Logic.Pathfinding.Obstacle import Obstacle

class GraphGeneratorTest(TestCase):

    def setUp(self):
        self.obstaclesList = [Obstacle((120,120)), Obstacle((130,300)), Obstacle((170,500)), Obstacle((335,200))]
        self.graphGenerator = GraphGenerator(self.obstaclesList,1000,600)
        self.graph = self.graphGenerator.generateGraph()

    def test_verifyReturnedGraphIsNotNull(self):
        self.assertTrue(self.graph != None)


    def test_everyNodeIsConnected(self):
        for compteur in range (0, self.graph.nodesList.__len__()):
            currentNode = self.graph.nodesList[compteur]
            self.assertTrue(currentNode.getConnectedNodesList().__len__() > 0)