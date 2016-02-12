from unittest import TestCase

from Client.BaseStation.Logic.Sequencer import Sequencer

import Client.BaseStation.Logic.State.SendingBotToChargingStationState as SendingBotToChargingStationState
import Client.BaseStation.Logic.State.SendingBotToTargetState as SendingBotToTargetState
import Client.BaseStation.Logic.State.SendingBotToTreasureState


class WorldVisionTest(TestCase):
    def test_givenAVisionTestWhenNothingThenNothing(self):
        return True