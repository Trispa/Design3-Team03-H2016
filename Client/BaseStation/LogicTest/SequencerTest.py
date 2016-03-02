from unittest import TestCase

from Client.BaseStation.Logic.Sequencer import Sequencer

import Client.BaseStation.Logic.State.SequencerState as SequencerState


class SequencerTest(TestCase):

    def test_whenCreatingSequencerThenStateIsSendingBotToChargingStation(self):
        testedSequencer = Sequencer()

        self.assertEqual(testedSequencer.state.__class__.__name__, "SendingBotToChargingStationState")


    def test_givenSequencerIsSendingBotToChargingStationWhenHandlingCurrentStateWithLastCoordinateThenStateBecomesSendingBotToTreasure(self):
        testedSequencer = Sequencer()
        testedSequencer.setState(
            SequencerState.SendingBotToChargingStationState())

        testedSequencer.handleCurrentState(testedSequencer.state.path.__len__() - 1)

        self.assertEqual(testedSequencer.state.__class__.__name__, "SendingBotToTreasureState")


    def test_givenSequencerSendingBotToTreasureWhenHandlingCurrentStateWithLastCoordinateThenStateBecomesSendingBotToTarget(self):
        testedSequencer = Sequencer()
        testedSequencer.setState(
            SequencerState.SendingBotToTreasureState())

        testedSequencer.handleCurrentState(testedSequencer.state.path.__len__() - 1)

        self.assertEqual(testedSequencer.state.__class__.__name__, "SendingBotToTargetState")


    def test_givenSequencerSendingBotToTargetWhenHandlingCurrentStateWithLastCoordinateThenStateBecomesSendingBotToChargingStation(self):
        testedSequencer = Sequencer()
        testedSequencer.setState(SequencerState.SendingBotToTargetState())

        testedSequencer.handleCurrentState(testedSequencer.state.path.__len__() - 1)

        self.assertEqual(testedSequencer.state.__class__.__name__, "SendingBotToChargingStationState")