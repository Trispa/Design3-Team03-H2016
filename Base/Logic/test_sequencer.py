from unittest import TestCase
import State.SendingBotToChargingStationState
import State.SendingBotToTargetState
import State.SendingBotToTreasureState
from Sequencer import Sequencer

class TestSequencer(TestCase):

    def test_whenCreatingSequencerThenStateIsAwaitingStart(self):
        testedSequencer = Sequencer()

        self.assertEqual(testedSequencer.myState.__class__.__name__, "SendingBotToChargingStationState")


    def test_givenSequencerIsSendingBotToChargingStationWhenHandlingCurrentStateThenStateBecomesSendingBotToTreasure(self):
        testedSequencer = Sequencer()
        testedSequencer.setState(State.SendingBotToChargingStationState.SendingBotToChargingStationState())

        testedSequencer.handleCurrentState()

        self.assertEqual(testedSequencer.myState.__class__.__name__, "SendingBotToTreasureState")


    def test_givenSequencerSendingBotToTreasureWhenHandlingCurrentStateThenStateBecomesSendingBotToTarget(self):
        testedSequencer = Sequencer()
        testedSequencer.setState(State.SendingBotToTreasureState.SendingBotToTreasureState())

        testedSequencer.handleCurrentState()

        self.assertEqual(testedSequencer.myState.__class__.__name__, "SendingBotToTargetState")


    def test_givenSequencerSendingBotToTargetWhenHandlingCurrentStateThenStateBecomesSendingBotToChargingStation(self):
        testedSequencer = Sequencer()
        testedSequencer.setState(State.SendingBotToTargetState.SendingBotToTargetState())

        testedSequencer.handleCurrentState()

        self.assertEqual(testedSequencer.myState.__class__.__name__, "SendingBotToChargingStationState")