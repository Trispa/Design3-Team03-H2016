from unittest import TestCase
from mock import MagicMock
from Client.Robot.Logic.WheelManager import WheelManager
from mock import patch
from mock import call

class WheelManagerTest(TestCase):
    AN_ANGLE = 90
    ZERO_ANGLE = 0

    A_POINT = (123,234)
    ORIGIN_POINT = (0,0)

    def setUp(self):
        self.wheelMotorMock = MagicMock()
        self.wheelManager = WheelManager(self.wheelMotorMock,self.wheelMotorMock,self.wheelMotorMock,self.wheelMotorMock)


    @patch('Client.Robot.Logic.WheelManager.SpeedCalculator.generateRotationInfos', autospec=True)
    def test_whenRotationIsCalledThenSetVitesseIsCalledOnEachWheelWithSameSpeed(self, speedCalculatorMock):
        theSpeed = 5
        speedCalculatorMock.return_value = theSpeed,0

        self.wheelManager.rotate(self.AN_ANGLE)
        calls = [call(5),call(5),call(5),call(5),call(0),call(0),call(0),call(0)]

        self.wheelMotorMock.setVitesse.assert_has_calls(calls)
        self.assertEqual(8, self.wheelMotorMock.setVitesse.call_count)


    def test_whenRotationIsCalledWithZeroThenSetVitesseIsntCalled(self):
        self.wheelManager.rotate(self.ZERO_ANGLE)

        self.wheelMotorMock.setVitesse.assert_not_called()


    @patch('Client.Robot.Logic.WheelManager.SpeedCalculator.generateSpeedInfos', autospec=True)
    def test_whenMoveToIsCalledThenSetVitesseIsCalledWithCorrectSpeed(self, speedCalculatorMock):
        theSpeedX = 5
        theSpeedY = 6
        speedCalculatorMock.return_value = theSpeedX, theSpeedY, 0

        self.wheelManager.moveTo(self.A_POINT)
        calls = [call(theSpeedX),call(-theSpeedX),call(theSpeedY),call(-theSpeedY), call(0),call(0),call(0),call(0)]

        self.wheelMotorMock.setVitesse.assert_has_calls(calls)


    def test_whenMoveToIsCalledWithOriginPointThenSetVitesseIsNotCalled(self):
        self.wheelManager.moveTo(self.ORIGIN_POINT)

        self.wheelMotorMock.setVitesse.assert_not_called()



