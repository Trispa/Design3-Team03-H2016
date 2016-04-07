from unittest import TestCase

from Client.BaseStation.Logic.Pathfinding.Graph.SafeZone import SafeZone


class SafeZoneTest(TestCase):
    def setUp(self):
        self.safeZone = SafeZone((0,0),(200,0),(0,100))
        
    def test_getGoodCenterOfZone(self):
        centerNode = self.safeZone.getCenterNodeOfSafeZone()
        theCenter = (100,50)
        self.assertEqual(centerNode.positionX, theCenter[0])
        self.assertEqual(centerNode.positionY, theCenter[1])