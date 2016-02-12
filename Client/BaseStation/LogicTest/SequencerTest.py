from unittest import TestCase

from Client.BaseStation.Logic.Sequencer import Sequencer

import Client.BaseStation.Logic.State.SendingBotToChargingStationState as SendingBotToChargingStationState
import Client.BaseStation.Logic.State.SendingBotToTargetState as SendingBotToTargetState
import Client.BaseStation.Logic.State.SendingBotToTreasureState


class SequencerTest(TestCase):

    def test_whenCreatingSequencerThenStateIsAwaitingStart(self):
        testedSequencer = Sequencer()

        self.assertEqual(testedSequencer.state.__class__.__name__, "SendingBotToChargingStationState")


    def test_givenSequencerIsSendingBotToChargingStationWhenHandlingCurrentStateThenStateBecomesSendingBotToTreasure(self):
        testedSequencer = Sequencer()
        testedSequencer.setState(
            SendingBotToChargingStationState.SendingBotToChargingStationState())

        testedSequencer.handleCurrentState()

        self.assertEqual(testedSequencer.state.__class__.__name__, "SendingBotToTreasureState")


    def test_givenSequencerSendingBotToTreasureWhenHandlingCurrentStateThenStateBecomesSendingBotToTarget(self):
        testedSequencer = Sequencer()
        testedSequencer.setState(
            Client.BaseStation.Logic.State.SendingBotToTreasureState.SendingBotToTreasureState())

        testedSequencer.handleCurrentState()

        self.assertEqual(testedSequencer.state.__class__.__name__, "SendingBotToTargetState")


    def test_givenSequencerSendingBotToTargetWhenHandlingCurrentStateThenStateBecomesSendingBotToChargingStation(self):
        testedSequencer = Sequencer()
        testedSequencer.setState(SendingBotToTargetState.SendingBotToTargetState())

        testedSequencer.handleCurrentState()

        self.assertEqual(testedSequencer.state.__class__.__name__, "SendingBotToChargingStationState")