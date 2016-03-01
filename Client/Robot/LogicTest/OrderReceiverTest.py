from unittest import TestCase
from mock import MagicMock
from Client.Robot.Logic.OrderReceiver import OrderReceiver
from mock import patch
from mock import call

class OrderReceiverTest(TestCase):

    def setUp(self):
        self.wheelManager = MagicMock()
        self.robot = MagicMock()
        self.orderReceiver = OrderReceiver(self.robot, self.wheelManager)

    def test_givenOrderReceiverWhenCreatedThenStateIsExecutingOrders(self):
        self.assertEquals('ExecutingOrderState', self.orderReceiver.state.__class__.__name__)


    # @patch('Client.Robot.Logic.WheelManager.SpeedCalculator.generateRotationInfos', autospec=True)
    # def test_whenRotationIsCalledThenSetVitesseIsCalledOnEachWheelWithSameSpeed(self, speedCalculatorMock):
    #     theSpeed = 5
    #     speedCalculatorMock.return_value = theSpeed,0
    #
    #     self.wheelManager.rotate(self.AN_ANGLE)
    #     calls = [call(5),call(5),call(5),call(5),call(0),call(0),call(0),call(0)]
    #
    #     self.wheelMotorMock.setVitesse.assert_has_calls(calls)
    #     self.assertEqual(8, self.wheelMotorMock.setVitesse.call_count)
    #
    #
    # def test_whenRotationIsCalledWithZeroThenSetVitesseIsntCalled(self):
    #     self.wheelManager.rotate(self.ZERO_ANGLE)
    #
    #     self.wheelMotorMock.setVitesse.assert_not_called()
    #
    #
    # @patch('Client.Robot.Logic.WheelManager.SpeedCalculator.generateSpeedInfos', autospec=True)
    # def test_whenMoveToIsCalledThenSetVitesseIsCalledWithCorrectSpeed(self, speedCalculatorMock):
    #     theSpeedX = 5
    #     theSpeedY = 6
    #     speedCalculatorMock.return_value = theSpeedX, theSpeedY, 0
    #
    #     self.wheelManager.moveTo(self.A_POINT)
    #     calls = [call(theSpeedX),call(-theSpeedX),call(theSpeedY),call(-theSpeedY), call(0),call(0),call(0),call(0)]
    #
    #     self.wheelMotorMock.setVitesse.assert_has_calls(calls)
    #
    #
    # def test_whenMoveToIsCalledWithOriginPointThenSetVitesseIsNotCalled(self):
    #     self.wheelManager.moveTo(self.ORIGIN_POINT)
    #
    #     self.wheelMotorMock.setVitesse.assert_not_called()



