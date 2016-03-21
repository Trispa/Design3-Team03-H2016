from unittest import TestCase

from Client.Robot.Logic.Deplacement.SpeedCalculator import SpeedCalculator


class SpeedCalculatorTest(TestCase):
    A_POINT = (145,256)
    ORIGIN_POINT = (0,0)

    AN_ANGLE = 90
    ZERO_ANGLE = 0

    def setUp(self):
        self.speedCalculator = SpeedCalculator()


    def test_givenAPointWhenGenerateSpeedInfosIsCalledThenReturnCorrectSpeedValues(self):
        speedX, speedY, timeforDeplacement = self.speedCalculator.generateSpeedInfos(self.A_POINT)

        totalDeplacement = float(self.A_POINT.__getitem__(0)+ self.A_POINT.__getitem__(1))
        correctSpeedX = (self.A_POINT.__getitem__(0)/totalDeplacement)*self.speedCalculator.VITESSE
        correctSpeedY = (self.A_POINT.__getitem__(1)/totalDeplacement)*self.speedCalculator.VITESSE
        correctTime = self.A_POINT.__getitem__(1)/correctSpeedY

        self.assertEqual(correctSpeedX, speedX)
        self.assertEqual(correctSpeedY, speedY)
        self.assertEqual(timeforDeplacement, correctTime)


    def test_givenOriginPointWhenGenerateSpeedInfosIsCalledThenReturnO(self):
        speedX, speedY, timeforDeplacement = self.speedCalculator.generateSpeedInfos(self.ORIGIN_POINT)

        correctSpeedX = 0
        correctSpeedY = 0
        correctTime = 0

        self.assertEqual(correctSpeedX, speedX)
        self.assertEqual(correctSpeedY, speedY)
        self.assertEqual(timeforDeplacement, correctTime)


    def test_givenAnAngleWhenGenerateRotationInfosIsCalledThenReturnCorrectValues(self):
        rotationSpeed, timeForRotation = self.speedCalculator.generateRotationInfos(self.AN_ANGLE)

        theCorrectRotationSpeed = self.speedCalculator.ROTATION_SPEED
        theCorrectRotationTime = float(self.AN_ANGLE)/360*self.speedCalculator.TIME_FOR_A_360

        self.assertEqual(theCorrectRotationSpeed, rotationSpeed)
        self.assertEqual(theCorrectRotationTime, timeForRotation)


    def test_givenA0AngleWhenGenerateRotationInfosIsCalledThenReturn0AsRotationTime(self):
        rotationSpeed, timeForRotation = self.speedCalculator.generateRotationInfos(self.ZERO_ANGLE)

        theCorrectRotationSpeed = self.speedCalculator.ROTATION_SPEED
        theCorrectRotationTime = 0

        self.assertEqual(theCorrectRotationSpeed, rotationSpeed)
        self.assertEqual(theCorrectRotationTime, timeForRotation)
