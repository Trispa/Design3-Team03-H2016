from unittest import TestCase
from mock import MagicMock
from Client.Robot.Logic.BotDispatcher import BotDispatcher


class BotDispatcherTest(TestCase):

    RANDOM_COORDINATE = {"positionFROMx" : 100,
                          "positionFROMy" : 100,
                          "positionTOx" : 200,
                          "positionTOy" : 200,
                          "orientation":90}

    def setUp(self):
        self.wheelManager = MagicMock()
        self.maestro = MagicMock()

    def test_whenFollowPathThenWheelManagerCallsMoveTo(self):
        testedBotDispatcher = BotDispatcher(self.wheelManager, self.maestro)
        testedBotDispatcher.followPath(self.RANDOM_COORDINATE)

        assert self.wheelManager.moveTo.called

    def test_whenSetRobotOrientationThenWheelManagerChangesOrientation(self):
        testedBotDispatcher = BotDispatcher(self.wheelManager, self.maestro)
        testedBotDispatcher.setRobotOrientation(90, 180)

        assert self.wheelManager.setOrientation.called