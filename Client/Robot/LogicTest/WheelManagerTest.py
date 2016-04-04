from unittest import TestCase

from mock import MagicMock
from mock import call
from mock import patch

from Client.Robot.Movement.WheelManager import WheelManager


class WheelManagerTest(TestCase):
    AN_ANGLE = 90
    ZERO_ANGLE = 0

    A_POINT = (123,234)
    ORIGIN_POINT = (0,0)


    def setUp(self):
        self.wheelMotorMock = MagicMock()
        self.serialPortCommunicator = MagicMock()
        self.wheelManager = WheelManager(self.serialPortCommunicator)


    def test_whenRotationIsCalledThenSetVitesseIsCalledOnEachWheelWithSameSpeed(self):
        theSpeed = 5

        self.assertEqual(5, theSpeed)


    def test_whenRotationIsCalledWithZeroThenSetVitesseIsntCalled(self):
        self.wheelManager.rotate(self.ZERO_ANGLE)

        self.wheelMotorMock.setVitesse.assert_not_called()


    # @patch('Client.Robot.Logic.WheelManager.SpeedCalculator.generateSpeedInfos', autospec=True)
    # def test_whenMoveToIsCalledThenSetVitesseIsCalledWithCorrectSpeed(self, speedCalculatorMock):
    #
    #     self.wheelManager.moveTo(self.A_POINT)
    #     calls = [call(self.A_POINT[0],self.A_POINT[1])]
    #
    #     self.moteurRoueMock.avanceVector.assert_has_calls(calls)


    def test_whenMoveToIsCalledWithOriginPointThenSetVitesseIsNotCalled(self):
        self.wheelManager.moveTo(self.ORIGIN_POINT)

        self.wheelMotorMock.setVitesse.assert_not_called()



