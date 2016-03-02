from unittest import TestCase
from mock import MagicMock
import sys


from Client.BaseStation.Logic.State import SequencerState


class SendingBotToTargetStateTest(TestCase):

    def test_whenCreatingSaidStateThenObstacleIndexIs0AndPathIsSet(self):
        testedState = SequencerState.SendingBotToTargetState()

        self.assertEqual(testedState.obstacleIndex, 0)
        self.assertIsNotNone(testedState.path)

    def test_whenCallingHandleOnSaidStateThenReturnCoordinatesWithTargetType(self):
        testedState = SequencerState.SendingBotToTargetState()
        sequencer = MagicMock()

        coordinates = testedState.handle(sequencer, 0)

        self.assertEquals(coordinates["type"], "target")

    def test_whenCallingHandleOnSaidStateWithThirdItemIndexThenReturnCoordinatesWithPositionTOCorrespondingAtTheCorrectCoordinatesFromPathList(self):
        testedState = SequencerState.SendingBotToTargetState()
        sequencer = MagicMock()

        coordinates = testedState.handle(sequencer, 0)

        self.assertEquals(coordinates["positionTO"]["positionX"], str(testedState.path[0][0]))
        self.assertEquals(coordinates["positionTO"]["positionY"], str(testedState.path[0][1]))

    def test_whenCallingHandleOnSaidStateWithLastItemThenSequencerIsCalledToChangeState(self):
        testedState = SequencerState.SendingBotToTargetState()
        sequencer = MagicMock()

        testedState.handle(sequencer, testedState.path.__len__() - 1)

        assert sequencer.setState.called

    def test_whenCallingHandleOnSaidStateWithFirstItemThenSequencerIsNotCalledToChangeState(self):
        testedState = SequencerState.SendingBotToTargetState()
        sequencer = MagicMock()

        testedState.handle(sequencer, 0)

        assert not sequencer.setState.called

    def test_whenCallingHandleOnSaidStateWithLastItemThenReturnedCoordinatesHasEndToYes(self):
        testedState = SequencerState.SendingBotToTargetState()
        sequencer = MagicMock()

        coordinates = testedState.handle(sequencer, testedState.path.__len__() - 1)

        self.assertEquals(coordinates["end"], "yes")

    def test_whenCallingHandleOnSaidStateWithLastItemThenReturnedCoordinatesHasIndexAtMinus1(self):
        testedState = SequencerState.SendingBotToTargetState()
        sequencer = MagicMock()

        coordinates = testedState.handle(sequencer, testedState.path.__len__() - 1)

        self.assertEquals(coordinates["index"], "-1")

    def test_whenCallingHandleOnSaidStateWithAnyItemThenReturnedCoordinatesHasIndexAtSameIndex(self):
        testedState = SequencerState.SendingBotToTargetState()
        sequencer = MagicMock()

        coordinates = testedState.handle(sequencer, 0)

        self.assertEquals(coordinates["index"], "0")