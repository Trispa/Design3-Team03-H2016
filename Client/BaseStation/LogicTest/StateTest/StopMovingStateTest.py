from unittest import TestCase

from mock import MagicMock

from Client.BaseStation.Logic import SequencerState


class StopMovingStateTest(TestCase):

    def setUp(self):
        self.pathfinder = MagicMock()
        self.sequencer = MagicMock()
        self.map = MagicMock()

    def test_whenHandlingSaidStateThenPathfinderIsNotCalled(self):
        testedState = SequencerState.StopMovingState()

        testedState.handle(self.sequencer,self.map, self.pathfinder)

        assert not self.pathfinder.findPath.called
        assert not self.sequencer.setState.called

    def test_whenHandlingSaidStateThenReturnsNoneAsNextSignal(self):
        testedState = SequencerState.StopMovingState()

        path, signal, orientation = testedState.handle(self.sequencer,self.map, self.pathfinder)

        self.assertEqual(None, signal)

    def test_whenHandlingSaidStateThenReturnsNoneAsOrientation(self):
        testedState = SequencerState.StopMovingState()

        path, signal, orientation = testedState.handle(self.sequencer,self.map, self.pathfinder)

        self.assertEqual(None, orientation)