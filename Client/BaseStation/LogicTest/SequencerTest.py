from unittest import TestCase

from Client.BaseStation.Logic.Sequencer import Sequencer

import Client.BaseStation.Logic.State.SequencerState as SequencerState


class SequencerTest(TestCase):

    def test_whenCreatingSequencerThenStateIsAwaitingStart(self):
        testedSequencer = Sequencer()

        self.assertEqual(testedSequencer.state.__class__.__name__, "SendingBotToChargingStationState")


    def test_givenSequencerIsSendingBotToChargingStationWhenHandlingCurrentStateThenStateBecomesSendingBotToTreasure(self):
        testedSequencer = Sequencer()
        testedSequencer.setState(
            SequencerState.SendingBotToChargingStationState())

        testedSequencer.handleCurrentState()

        self.assertEqual(testedSequencer.state.__class__.__name__, "SendingBotToTreasureState")


    def test_givenSequencerSendingBotToTreasureWhenHandlingCurrentStateThenStateBecomesSendingBotToTarget(self):
        testedSequencer = Sequencer()
        testedSequencer.setState(
            SequencerState.SendingBotToTreasureState())

        testedSequencer.handleCurrentState()

        self.assertEqual(testedSequencer.state.__class__.__name__, "SendingBotToTargetState")


    def test_givenSequencerSendingBotToTargetWhenHandlingCurrentStateThenStateBecomesSendingBotToChargingStation(self):
        testedSequencer = Sequencer()
        testedSequencer.setState(SequencerState.SendingBotToTargetState())

        testedSequencer.handleCurrentState()

        self.assertEqual(testedSequencer.state.__class__.__name__, "SendingBotToChargingStationState")