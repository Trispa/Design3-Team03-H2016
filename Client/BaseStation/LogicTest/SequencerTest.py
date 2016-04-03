from unittest import TestCase
from mock import MagicMock
from Client.BaseStation.Logic.SequencerState import *
from Client.BaseStation.Logic.Sequencer import Sequencer


class SequencerTest(TestCase):

    def setUp(self):
        self.pathfinder = MagicMock()
        self.stateMock = MagicMock()
        self.mapMock = MagicMock()
    def test_whenCreatingSequencerThenStateIsSendingBotToChargingStation(self):
        testedSequencer = Sequencer(self.pathfinder)

        self.assertTrue(isinstance(testedSequencer.state, SendingBotToChargingStationState))

    def test_whenHandlingSequencerThenStateCallsHandle(self):
        testedSequencer = Sequencer(self.pathfinder)
        testedSequencer.setState(self.stateMock)
        testedSequencer.handleCurrentState(self.mapMock)

        assert self.stateMock.handle.called