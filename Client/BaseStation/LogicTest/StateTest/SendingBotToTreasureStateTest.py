from unittest import TestCase
from mock import MagicMock

from Client.BaseStation.Logic.State import SequencerState


class SendingBotToTreasureStateTest(TestCase):

    def test_whenCreatingSaidStateThenObstacleIndexIs0AndPathIsSet(self):
        testedState = SequencerState.SendingBotToTreasureState()

        self.assertEqual(testedState.obstacleIndex, 0)
        self.assertIsNotNone(testedState.path)

    def test_whenCallingHandleOnSaidStateThenReturnCoordinatesWithTreasureType(self):
        testedState = SequencerState.SendingBotToTreasureState()
        sequencer = MagicMock()

        coordinates = testedState.handle(sequencer, 0)

        self.assertEquals(coordinates["type"], "treasure")

    def test_whenCallingHandleOnSaidStateWithFirstItemIndexThenReturnCoordinatesWithPositionTOCorrespondingAtTheCorrectCoordinatesFromPathList(self):
        testedState = SequencerState.SendingBotToTreasureState()
        sequencer = MagicMock()

        coordinates = testedState.handle(sequencer, 0)

        self.assertEquals(coordinates["positionTO"]["positionX"], str(testedState.path[0][0]))
        self.assertEquals(coordinates["positionTO"]["positionY"], str(testedState.path[0][1]))

    def test_whenCallingHandleOnSaidStateWithLastItemThenSequencerIsCalledToChangeState(self):
        testedState = SequencerState.SendingBotToTreasureState()
        sequencer = MagicMock()

        testedState.handle(sequencer, testedState.path.__len__() - 1)

        assert sequencer.setState.called

    def test_whenCallingHandleOnSaidStateWithFirstItemThenSequencerIsNotCalledToChangeState(self):
        testedState = SequencerState.SendingBotToTreasureState()
        sequencer = MagicMock()

        testedState.handle(sequencer, 0)

        assert not sequencer.setState.called

    def test_whenCallingHandleOnSaidStateWithLastItemThenReturnedCoordinatesHasEndToNo(self):
        testedState = SequencerState.SendingBotToTreasureState()
        sequencer = MagicMock()

        coordinates = testedState.handle(sequencer, testedState.path.__len__() - 1)

        self.assertEquals(coordinates["end"], "no")

    def test_whenCallingHandleOnSaidStateWithLastItemThenReturnedCoordinatesHasIndexAtMinus1(self):
        testedState = SequencerState.SendingBotToTreasureState()
        sequencer = MagicMock()

        coordinates = testedState.handle(sequencer, testedState.path.__len__() - 1)

        self.assertEquals(coordinates["index"], "-1")

    def test_whenCallingHandleOnSaidStateWithAnyItemThenReturnedCoordinatesHasIndexAtSameIndex(self):
        testedState = SequencerState.SendingBotToTreasureState()
        sequencer = MagicMock()

        coordinates = testedState.handle(sequencer, 0)

        self.assertEquals(coordinates["index"], "0")