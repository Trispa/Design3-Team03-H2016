from unittest import TestCase
import Base.Logic.State.SendingBotToChargingStationState
import Base.Logic.State.SendingBotToTargetState
import Base.Logic.State.SendingBotToTreasureState
from Base.Logic.Sequencer import Sequencer

class SequencerTest(TestCase):

    def test_whenCreatingSequencerThenStateIsAwaitingStart(self):
        testedSequencer = Sequencer()

        self.assertEqual(testedSequencer.myState.__class__.__name__, "SendingBotToChargingStationState")


    def test_givenSequencerIsSendingBotToChargingStationWhenHandlingCurrentStateThenStateBecomesSendingBotToTreasure(self):
        testedSequencer = Sequencer()
        testedSequencer.setState(Base.Logic.State.SendingBotToChargingStationState.SendingBotToChargingStationState())

        testedSequencer.handleCurrentState()

        self.assertEqual(testedSequencer.myState.__class__.__name__, "SendingBotToTreasureState")


    def test_givenSequencerSendingBotToTreasureWhenHandlingCurrentStateThenStateBecomesSendingBotToTarget(self):
        testedSequencer = Sequencer()
        testedSequencer.setState(Base.Logic.State.SendingBotToTreasureState.SendingBotToTreasureState())

        testedSequencer.handleCurrentState()

        self.assertEqual(testedSequencer.myState.__class__.__name__, "SendingBotToTargetState")


    def test_givenSequencerSendingBotToTargetWhenHandlingCurrentStateThenStateBecomesSendingBotToChargingStation(self):
        testedSequencer = Sequencer()
        testedSequencer.setState(Base.Logic.State.SendingBotToTargetState.SendingBotToTargetState())

        testedSequencer.handleCurrentState()

        self.assertEqual(testedSequencer.myState.__class__.__name__, "SendingBotToChargingStationState")