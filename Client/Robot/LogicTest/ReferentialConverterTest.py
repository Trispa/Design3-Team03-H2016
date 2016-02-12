from unittest import TestCase
from Client.Robot.Logic.ReferentialConverter import ReferentialConverter

class ReferentialConverterTest(TestCase):
    DEFAULT_POINT = (100,100)
    DEFAULT_ORIENTATION = 90

    ANOTHER_POINT = (150,200)
    ANOTHER_ORIENTATION = 75

    def setUp(self):
        self.referentialConverter = ReferentialConverter(self.DEFAULT_POINT, self.DEFAULT_ORIENTATION)

    def test_whenCreatingReferentialConverterThenClassAttributesAreSetCorrectly(self):
        positionX = self.referentialConverter.positionRobotInWorldX
        positionY = self.referentialConverter.positionRobotInWorldY
        orientation = self.referentialConverter.orientation
        defaultOrientation = (float("{0:.3f}".format(float(self.DEFAULT_ORIENTATION%360)/180)))

        self.assertEqual(self.DEFAULT_POINT.__getitem__(0), positionX)
        self.assertEqual(self.DEFAULT_POINT.__getitem__(1), positionY)
        self.assertEqual(defaultOrientation, orientation)


    def test_whenSettingPositionThenPositionIsSetWithSaidData(self):
        self.referentialConverter = ReferentialConverter(self.ANOTHER_POINT, self.ANOTHER_ORIENTATION)

        thePoint = self.ANOTHER_POINT
        theOrientation = (float("{0:.3f}".format(float(self.ANOTHER_ORIENTATION%360)/180)))
        positionX = self.referentialConverter.positionRobotInWorldX
        positionY = self.referentialConverter.positionRobotInWorldY
        orientation = self.referentialConverter.orientation

        self.assertEqual(thePoint.__getitem__(0), positionX)
        self.assertEqual(thePoint.__getitem__(1), positionY)
        self.assertEqual(theOrientation, orientation)


    def test_givenDefaultPointToBeCovertedWithDefaultOrientationWhenConverWorldToRobotThenPointIsConvertedCorrectly(self):
        pointConverted = self.referentialConverter.convertWorldToRobot(self.DEFAULT_POINT)
        ConvertedPointShouldBe = (0,0)

        self.assertEqual(ConvertedPointShouldBe.__getitem__(0), pointConverted.__getitem__(0).__getitem__(0))
        self.assertEqual(ConvertedPointShouldBe.__getitem__(1), pointConverted.__getitem__(1).__getitem__(0))



    def test_givenNotDefaultPointToBeCovertedWithDefaultOrientationWhenConverWorldToRobotThenPointIsConvertedCorrectly(self):
        pointConverted = self.referentialConverter.convertWorldToRobot(self.ANOTHER_POINT)
        ConvertedPointShouldBe = (-100,50)

        self.assertEqual(ConvertedPointShouldBe.__getitem__(0), pointConverted.__getitem__(0).__getitem__(0))
        self.assertEqual(ConvertedPointShouldBe.__getitem__(1), pointConverted.__getitem__(1).__getitem__(0))