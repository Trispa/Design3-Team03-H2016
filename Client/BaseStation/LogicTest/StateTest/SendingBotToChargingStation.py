from unittest import TestCase
from mock import MagicMock

from Client.BaseStation.Logic.State.SendingBotToChargingStationState import SendingBotToChargingStationState


class SendingBotToChargingStationStateTest(TestCase):

    def test_whenCreatingSaidStateThenObstacleIndexIs0AndPathIsSet(self):
        testedState = SendingBotToChargingStationState()

        self.assertEqual(testedState.obstacleIndex, 0)
        self.assertIsNotNone(testedState.path)

    def test_whenCallingHandleOnSaidStateThenReturnCoordinatesWithChargingStationType(self):
        testedState = SendingBotToChargingStationState()
        sequencer = MagicMock()

        coordinates = testedState.handle(sequencer, 0)

        self.assertEquals(coordinates["type"], "charging station")

    def test_whenCallingHandleOnSaidStateWithThirdItemIndexThenReturnCoordinatesWithPositionTOCorrespondingAtTheCorrectCoordinatesFromPathList(self):
        thirdItem = 2
        testedState = SendingBotToChargingStationState()
        sequencer = MagicMock()

        coordinates = testedState.handle(sequencer, thirdItem)

        self.assertEquals(coordinates["positionTO"]["positionX"], str(testedState.path[thirdItem][0]))
        self.assertEquals(coordinates["positionTO"]["positionY"], str(testedState.path[thirdItem][1]))

    def test_whenCallingHandleOnSaidStateWithLastItemThenSequencerIsCalledToChangeState(self):
        testedState = SendingBotToChargingStationState()
        sequencer = MagicMock()

        testedState.handle(sequencer, testedState.path.__len__() - 1)

        assert sequencer.setState.called

    def test_whenCallingHandleOnSaidStateWithFirstItemThenSequencerIsNotCalledToChangeState(self):
        testedState = SendingBotToChargingStationState()
        sequencer = MagicMock()

        testedState.handle(sequencer, 0)

        assert not sequencer.setState.called

    def test_whenCallingHandleOnSaidStateWithLastItemThenReturnedCoordinatesHasEndToNo(self):
        testedState = SendingBotToChargingStationState()
        sequencer = MagicMock()

        coordinates = testedState.handle(sequencer, testedState.path.__len__() - 1)

        self.assertEquals(coordinates["end"], "no")

    def test_whenCallingHandleOnSaidStateWithLastItemThenReturnedCoordinatesHasIndexAtMinus1(self):
        testedState = SendingBotToChargingStationState()
        sequencer = MagicMock()

        coordinates = testedState.handle(sequencer, testedState.path.__len__() - 1)

        self.assertEquals(coordinates["index"], "-1")

    def test_whenCallingHandleOnSaidStateWithAnyItemThenReturnedCoordinatesHasIndexAtSameIndex(self):
        testedState = SendingBotToChargingStationState()
        sequencer = MagicMock()

        coordinates = testedState.handle(sequencer, 4)

        self.assertEquals(coordinates["index"], "4")