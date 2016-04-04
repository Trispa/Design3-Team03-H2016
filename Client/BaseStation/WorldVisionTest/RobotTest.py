from unittest import TestCase
from mock import MagicMock
from Client.BaseStation.WorldVision.Robot import Robot


class RobotMock(TestCase):

    def setUp(self):
        self.circle = MagicMock()
        self.square = MagicMock()
        self.circle.getContour.return_value = [0,1,2]
        self.square.getContour.return_value = [0,1,2]
        self.robot = Robot(self.square, self.circle)

    def test_givenCoordinatesFormingAVectorGoingToTheBottomRightWhenSettingOrientationThenOrientationIs45(self):
        self.circle.findCenterOfMass.return_value = (100, 100)
        self.square.findCenterOfMass.return_value = (200, 200)

        self.robot.setOrientation()

        self.assertEqual(self.robot.orientation, 180)


    def test_givenCoordinatesFormingAVectorGoingToTheTopRightWhenSettingOrientationThenOrientationIs315(self):
        self.circle.findCenterOfMass.return_value = (200, 200)
        self.square.findCenterOfMass.return_value = (300, 100)

        self.robot.setOrientation()

        self.assertEqual(self.robot.orientation, 90)

    def test_givenCoordinatesFormingAVectorGoingToTheTopLeftWhenSettingOrientationThenOrientationIs225(self):
        self.circle.findCenterOfMass.return_value = (200, 200)
        self.square.findCenterOfMass.return_value = (100, 100)

        self.robot.setOrientation()

        self.assertEqual(self.robot.orientation, 0)

    def test_givenCoordinatesFormingAVectorGoingToTheBottomLeftWhenSettingOrientationThenOrientationIs135(self):
        self.circle.findCenterOfMass.return_value = (200, 200)
        self.square.findCenterOfMass.return_value = (100, 300)

        self.robot.setOrientation()

        self.assertEqual(self.robot.orientation, 270)

    def test_givenCoordinatesFormingAVectorGoingToTheLeftWhenSettingOrientationThenOrientationIs180(self):
        self.circle.findCenterOfMass.return_value = (200, 300)
        self.square.findCenterOfMass.return_value = (100, 300)

        self.robot.setOrientation()

        self.assertEqual(self.robot.orientation, 315)

    def test_givenCoordinatesFormingAVectorGoingToTheRightWhenSettingOrientationThenOrientationIs0(self):
        self.circle.findCenterOfMass.return_value = (200, 300)
        self.square.findCenterOfMass.return_value = (300, 300)

        self.robot.setOrientation()

        self.assertEqual(self.robot.orientation, 135)

    def test_givenCoordinatesFormingAVectorGoingToTheTopWhenSettingOrientationThenOrientationIs270(self):
        self.circle.findCenterOfMass.return_value = (200, 200)
        self.square.findCenterOfMass.return_value = (200, 100)

        self.robot.setOrientation()

        self.assertEqual(self.robot.orientation, 45)

    def test_givenCoordinatesFormingAVectorGoingToTheBottomWhenSettingOrientationThenOrientationIs90(self):
        self.circle.findCenterOfMass.return_value = (200, 200)
        self.square.findCenterOfMass.return_value = (200, 300)

        self.robot.setOrientation()

        self.assertEqual(self.robot.orientation, 225)

    def test_givenCoordinatesFormingAVectorGoingToTheBottomWhenSettingCenterThenCenterIsMiddleOfVector(self):
        self.circle.findCenterOfMass.return_value = (200, 200)
        self.square.findCenterOfMass.return_value = (300, 300)

        self.robot.setCenter()

        self.assertEqual(self.robot.center, (250,250))