from unittest import TestCase

from mock import MagicMock

from Client.BaseStation.Logic import SequencerState


class DetectTreasureStateTest(TestCase):

    def setUp(self):
        self.pathfinder = MagicMock()
        self.sequencer = MagicMock()
        self.map = MagicMock()

    def test_whenHandlingSaidStateThenPathfinderIsCalled(self):
        testedState = SequencerState.DetectTreasureState()

        testedState.handle(self.sequencer,self.map, self.pathfinder)

        assert self.pathfinder.findPath.called
        assert self.sequencer.setState.called

    def test_whenHandlingSaidStateThenReturnsCorrectNextSignalInSequence(self):
        testedState = SequencerState.DetectTreasureState()

        path, signal, orientation = testedState.handle(self.sequencer,self.map, self.pathfinder)

        self.assertEqual("detectTreasure", signal)

    def test_whenHandlingSaidStateThenReturnsCorrectOrientationToGiveRobot(self):
        testedState = SequencerState.DetectTreasureState()

        path, signal, orientation = testedState.handle(self.sequencer,self.map, self.pathfinder)

        self.assertEqual(180, orientation)