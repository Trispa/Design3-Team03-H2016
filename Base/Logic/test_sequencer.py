from unittest import TestCase
from State.AwaitingStartState import AwaitingStartState
from Sequencer import Sequencer

class TestSequencer(TestCase):
    # def test_setState(self):
    #     self.fail()
    #
    # def test_Sequencer(self):
    #     self.fail()
    #
    # def test_handleCurrentState(self):
    #     self.fail()

    def test_whenCreatingSequencerThenStateIsAwaitingStart(self):
        testedSequencer = Sequencer()

        self.assertEqual(testedSequencer.myState.__class__.__name__, "AwaitingStartState")

    def test_whenAssignNextStateOnFreshlyBuiltSequencerThenStateIsSendingBotToChargingStation(self):
        testedSequencer = Sequencer()
        testedSequencer.assignNextState()

        self.assertEqual(testedSequencer.myState.__class__.__name__, "SendingBotToChargingStationState")

    def test_whenAssignNextStateTwoTimesSequencerThenStateIsAwaitingTarget(self):
        testedSequencer = Sequencer()
        testedSequencer.assignNextState()
        testedSequencer.assignNextState()

        self.assertEqual(testedSequencer.myState.__class__.__name__, "AwaitingTargetState")

    def test_whenAssignNextStateTwoTimesSequencerThenStateIsAwaitingTarget(self):
        testedSequencer = Sequencer()
        testedSequencer.assignNextState()
        testedSequencer.assignNextState()

        self.assertEqual(testedSequencer.myState.__class__.__name__, "AwaitingTargetState")
