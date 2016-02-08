from unittest import TestCase
import State.AwaitingStartState
import State.AwaitingBotGraspingTreasureState
import State.SendingBotToChargingStationState
import State.AwaitingTargetState
import State.SendingBotToTargetState
import State.SendingBotToTreasureState
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

    def test_givenSequencerAwaitingStartWhenAssignNextStateSequencerThenStateIsSendingBotToChargingStation(self):
        testedSequencer = Sequencer()
        testedSequencer.setState(State.AwaitingStartState.AwaitingStartState())

        testedSequencer.assignNextState()

        self.assertEqual(testedSequencer.myState.__class__.__name__, "SendingBotToChargingStationState")

    def test_givenSequencerIsSendingBotToChargingStationWhenAssignNextStateOnSequencerThenStateIsAwaitingTarget(self):
        testedSequencer = Sequencer()
        testedSequencer.setState(State.SendingBotToChargingStationState.SendingBotToChargingStationState())

        testedSequencer.assignNextState()

        self.assertEqual(testedSequencer.myState.__class__.__name__, "AwaitingTargetState")

    def test_givenSequencerAwaitingTargetWhenAssignNextStateOnSequencerThenStateIsSendingBotToTreasure(self):
        testedSequencer = Sequencer()
        testedSequencer.setState(State.AwaitingTargetState.AwaitingTargetState())

        testedSequencer.assignNextState()

        self.assertEqual(testedSequencer.myState.__class__.__name__, "SendingBotToTreasureState")

    def test_givenSequencerSendingBotToTreasureWhenAssignNextStateOnSequencerThenStateIsAwaitingBotGraspingTreasure(self):
        testedSequencer = Sequencer()
        testedSequencer.setState(State.SendingBotToTreasureState.SendingBotToTreasureState())

        testedSequencer.assignNextState()

        self.assertEqual(testedSequencer.myState.__class__.__name__, "AwaitingBotGraspingTreasureState")

    def test_givenSequencerAwaitingBotGraspingTreasureWhenAssignNextStateOnSequencerThenStateIsSendingBotToTarget(self):
        testedSequencer = Sequencer()
        testedSequencer.setState(State.AwaitingBotGraspingTreasureState.AwaitingBotGraspingTreasureState())

        testedSequencer.assignNextState()

        self.assertEqual(testedSequencer.myState.__class__.__name__, "SendingBotToTargetState")

    def test_givenSequencerSendingBotToTargetWhenAssignNextStateOnSequencerThenStateIsAwaitingStart(self):
        testedSequencer = Sequencer()
        testedSequencer.setState(State.SendingBotToTargetState.SendingBotToTargetState())

        testedSequencer.assignNextState()

        self.assertEqual(testedSequencer.myState.__class__.__name__, "AwaitingStartState")