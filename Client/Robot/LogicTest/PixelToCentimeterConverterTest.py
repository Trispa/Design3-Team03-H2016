from unittest import TestCase

from Client.Robot.Movement.PixelToCentimeterConverter import PixelToCentimeterConverter

class PixelToCentimeterConverterTest(TestCase):

    def setUp(self):
        self.converter = PixelToCentimeterConverter()

    def test_convertAPoint(self):
        convertedPoint = self.converter.convertPixelToCentimeter((100,120))
        goodRatio = 49/9.5
        self.assertEqual(convertedPoint[0], 100/goodRatio)
        self.assertEqual(convertedPoint[1], 120/goodRatio)