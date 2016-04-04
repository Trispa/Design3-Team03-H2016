from unittest import TestCase

from mock import MagicMock
from mock import call
from mock import patch

from Client.Robot.Movement.WheelManager import WheelManager


class WheelManagerTest(TestCase):
    AN_ANGLE = 5
    ZERO_ANGLE = 0

    A_POINT = (5,5)
    ORIGIN_POINT = (0,0)


    def setUp(self):
        self.wheelMotorMock = MagicMock()
        self.serialPortCommunicator = MagicMock()
        self.wheelManager = WheelManager(self.serialPortCommunicator)


    def test_whenMoveInfiniteIsCalledOnAPointThenVitesseIsSet(self):
        self.wheelManager.moveForever(2,2)

        self.assertTrue(self.serialPortCommunicator.driveMoteurLine.call_count != 0)



    def test_whenMoveToIsCalledOnAPointThenVitesseIsSet(self):
        self.wheelManager.moveTo(self.A_POINT)

        self.assertTrue(self.serialPortCommunicator.driveMoteurLine.call_count != 0)


    def test_whenRotationIsCalledThenSetVitesse(self):
        self.wheelManager.rotate(self.AN_ANGLE)

        self.assertTrue(self.serialPortCommunicator.driveMoteurRotation.call_count == 1)


    def test_whenMoveToIsCalledOnTheCurrentPositionThenVitesseNotSet(self):
        self.wheelManager.moveTo(self.ORIGIN_POINT)

        self.assertTrue(self.serialPortCommunicator.driveMoteurLine.call_count == 0)


    def test_setOrientationThenGoodRotation(self):
        self.wheelManager.setOrientation(90,91)
        self.assertTrue(self.serialPortCommunicator.driveMoteurRotation.call_count == 1)



