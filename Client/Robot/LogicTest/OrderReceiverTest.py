from unittest import TestCase
from mock import MagicMock
from Client.Robot.Logic.OrderReceiver import OrderReceiver
from Client.Robot.Logic.ReferentialConverter import ReferentialConverter
import array
from mock import patch
from mock import call

class OrderReceiverTest(TestCase):

    RANDOM_COORDINATES = {"type": "charging station",
                          "positionTO": {
                              "positionX": "15",
                              "positionY": "15"},
                          "positionFROM": {
                              "positionX": "0",
                              "positionY": "0",
                              "orientation": "0"},
                          }

    def setUp(self):
        self.wheelManager = MagicMock()
        self.robot = MagicMock()
        self.orderReceiver = OrderReceiver(self.robot, self.wheelManager)

    def test_givenOrderReceiverWhenCreatedThenStateIsExecutingOrders(self):
        self.assertEquals('ExecutingOrderState', self.orderReceiver.state.__class__.__name__)

    def test_givenOrderReceiverWhenRefuseOrdersThenStateOfOrderReceiverIsRefusingOrders(self):
        self.orderReceiver.refuseOrders()

        self.assertEquals('RefusingOrderState', self.orderReceiver.state.__class__.__name__)

    def test_givenOrderReceiverWhenAcceptingOrdersThenStateOfOrderReceiverIsExecutingOrders(self):
        self.orderReceiver.acceptOrders()

        self.assertEquals('ExecutingOrderState', self.orderReceiver.state.__class__.__name__)

    def test_givenOrderReceiverWhenHandlingCurrentStateAtExecutingOrdersThenWheelManagerMoveToCoordinates(self):
        self.orderReceiver.handleCurrentState(self.RANDOM_COORDINATES)

        assert self.wheelManager.moveTo.called


    def test_givenOrderReceiverWhenHandlingCurrentStateAtRefusingOrdersThenWheelManagerDoesNotMove(self):
        self.orderReceiver.refuseOrders()
        self.orderReceiver.handleCurrentState(self.RANDOM_COORDINATES)

        assert not self.wheelManager.moveTo.called

    def test_givenOrderReceiverWhenHandlingCurrentStateWithChargingStationCoordinateThenStateIsExecutingOrders(self):
        self.RANDOM_COORDINATES['type'] = "charging station"
        self.orderReceiver.handleCurrentState(self.RANDOM_COORDINATES)

        self.assertEquals('ExecutingOrderState', self.orderReceiver.state.__class__.__name__)

    def test_givenOrderReceiverWhenHandlingCurrentStateWithTreasureCoordinateThenStateIsExecutingOrders(self):
        self.RANDOM_COORDINATES['type'] = "treasure"
        self.orderReceiver.handleCurrentState(self.RANDOM_COORDINATES)

        self.assertEquals('ExecutingOrderState', self.orderReceiver.state.__class__.__name__)

    def test_givenOrderReceiverWhenHandlingCurrentStateWithTargetCoordinateThenStateIsRefusingOrders(self):
        self.RANDOM_COORDINATES['type'] = "target"
        self.orderReceiver.handleCurrentState(self.RANDOM_COORDINATES)

        self.assertEquals('RefusingOrderState', self.orderReceiver.state.__class__.__name__)