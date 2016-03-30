from unittest import TestCase
from mock import MagicMock
from Client.Robot.Logic.BotDispatcher import BotDispatcher


class OrderReceiverTest(TestCase):

    RANDOM_COORDINATES = {"type": "charging station",
                          "endOfPhase":"no",
                          "index":"0",
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
        self.orderReceiver = BotDispatcher(self.robot, self.wheelManager)

    def test_givenOrderReceiverWhenCreatedThenStateIsExecutingOrders(self):
        self.assertEquals('ExecutingOrderState', self.orderReceiver.state.__class__.__name__)

    def test_givenOrderReceiverWhenRefuseOrdersThenStateOfOrderReceiverIsRefusingOrders(self):
        self.orderReceiver.refuseOrders()

        self.assertEquals('RefusingOrderState', self.orderReceiver.state.__class__.__name__)

    def test_givenOrderReceiverWhenAcceptingOrdersThenStateOfOrderReceiverIsExecutingOrders(self):
        self.orderReceiver.acceptOrders()

        self.assertEquals('ExecutingOrderState', self.orderReceiver.state.__class__.__name__)

    def test_givenOrderReceiverWhenHandlingCurrentStateAtExecutingOrdersThenWheelManagerMoveToCoordinates(self):
        self.orderReceiver.followPath(self.RANDOM_COORDINATES)

        assert self.wheelManager.moveTo.called


    def test_givenOrderReceiverWhenHandlingCurrentStateAtRefusingOrdersThenWheelManagerDoesNotMove(self):
        self.orderReceiver.refuseOrders()
        self.orderReceiver.followPath(self.RANDOM_COORDINATES)

        assert not self.wheelManager.moveTo.called

    def test_givenOrderReceiverWhenHandlingCurrentStateWithChargingStationCoordinateThenStateIsExecutingOrders(self):
        self.RANDOM_COORDINATES['type'] = "charging station"
        self.orderReceiver.followPath(self.RANDOM_COORDINATES)

        self.assertEquals('ExecutingOrderState', self.orderReceiver.state.__class__.__name__)

    def test_givenOrderReceiverWhenHandlingCurrentStateWithTreasureCoordinateThenStateIsExecutingOrders(self):
        self.RANDOM_COORDINATES['type'] = "treasure"
        self.RANDOM_COORDINATES['endOfPhase'] = "no"
        self.orderReceiver.followPath(self.RANDOM_COORDINATES)

        self.assertEquals('ExecutingOrderState', self.orderReceiver.state.__class__.__name__)

    def test_givenOrderReceiverWhenHandlingCurrentStateWithEndCoordinateThenStateIsRefusingOrders(self):
        self.RANDOM_COORDINATES['endOfPhase'] = "yes"
        self.orderReceiver.followPath(self.RANDOM_COORDINATES)

        self.assertEquals('RefusingOrderState', self.orderReceiver.state.__class__.__name__)