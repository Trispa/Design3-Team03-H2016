from unittest import TestCase

import Base.Client.BaseClient.Logic.State.SendingBotToChargingStationState as SendingBotToChargingStationState
import Base.Client.BaseClient.Logic.State.SendingBotToTargetState as SendingBotToTargetState
from Base.Client.BaseClient.Logic.Sequencer import Sequencer

import Base.Client.BaseClient.Logic.State.SendingBotToTreasureState


class SequencerTest(TestCase):

    def test_whenCreatingSequencerThenStateIsAwaitingStart(self):
        testedSequencer = Sequencer()

        self.assertEqual(testedSequencer.myState.__class__.__name__, "SendingBotToChargingStationState")


    def test_givenSequencerIsSendingBotToChargingStationWhenHandlingCurrentStateThenStateBecomesSendingBotToTreasure(self):
        testedSequencer = Sequencer()
        testedSequencer.setState(
            SendingBotToChargingStationState.SendingBotToChargingStationState())

        testedSequencer.handleCurrentState()

        self.assertEqual(testedSequencer.myState.__class__.__name__, "SendingBotToTreasureState")


    def test_givenSequencerSendingBotToTreasureWhenHandlingCurrentStateThenStateBecomesSendingBotToTarget(self):
        testedSequencer = Sequencer()
        testedSequencer.setState(
            Base.Client.BaseClient.Logic.State.SendingBotToTreasureState.SendingBotToTreasureState())

        testedSequencer.handleCurrentState()

        self.assertEqual(testedSequencer.myState.__class__.__name__, "SendingBotToTargetState")


    def test_givenSequencerSendingBotToTargetWhenHandlingCurrentStateThenStateBecomesSendingBotToChargingStation(self):
        testedSequencer = Sequencer()
        testedSequencer.setState(SendingBotToTargetState.SendingBotToTargetState())

        testedSequencer.handleCurrentState()

        self.assertEqual(testedSequencer.myState.__class__.__name__, "SendingBotToChargingStationState")