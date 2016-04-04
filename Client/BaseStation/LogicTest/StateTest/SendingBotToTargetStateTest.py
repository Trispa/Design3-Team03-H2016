from unittest import TestCase

from mock import MagicMock

from Client.BaseStation.Logic import SequencerState


class SendingBotToTargetStateTest(TestCase):

    def setUp(self):
        self.pathfinder = MagicMock()
        self.sequencer = MagicMock()
        self.map = MagicMock()

    def test_whenHandlingSaidStateThenPathfinderIsCalled(self):
        testedState = SequencerState.SendingBotToTargetState()

        testedState.handle(self.sequencer,self.map, self.pathfinder)

        assert self.pathfinder.findPath.called
        assert self.sequencer.setState.called

    def test_whenHandlingSaidStateThenReturnsCorrectNextSignalInSequence(self):
        testedState = SequencerState.SendingBotToTargetState()

        path, signal, orientation = testedState.handle(self.sequencer,self.map, self.pathfinder)

        self.assertEqual("alignPositionToTarget", signal)

    def test_whenHandlingSaidStateThenReturnsCorrectOrientationToGiveRobot(self):
        testedState = SequencerState.SendingBotToTargetState()

        path, signal, orientation = testedState.handle(self.sequencer,self.map, self.pathfinder)

        self.assertEqual(90, orientation)