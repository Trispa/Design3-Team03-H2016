from unittest import TestCase

from mock import MagicMock

from Client.BaseStation.Logic import SequencerState


class SendingBotToTreasureStateTest(TestCase):

    def setUp(self):
        self.pathfinder = MagicMock()
        self.sequencer = MagicMock()
        self.map = MagicMock()

        self.map.getPositionInFrontOfTreasure.return_value = (100,100), 270

    def test_whenHandlingSaidStateThenPathfinderIsCalled(self):
        testedState = SequencerState.SendingBotToTreasureState()

        testedState.handle(self.sequencer,self.map, self.pathfinder)

        assert self.pathfinder.findPath.called
        assert self.sequencer.setState.called

    def test_whenHandlingSaidStateThenReturnsCorrectNextSignalInSequence(self):
        testedState = SequencerState.SendingBotToTreasureState()

        path, signal, orientation = testedState.handle(self.sequencer,self.map, self.pathfinder)

        self.assertEqual("rotateToTreasure", signal)

    def test_whenHandlingSaidStateThenReturnsCorrectOrientationToGiveRobot(self):
        testedState = SequencerState.SendingBotToTreasureState()

        path, signal, orientation = testedState.handle(self.sequencer,self.map, self.pathfinder)

        self.assertEqual(270, orientation)