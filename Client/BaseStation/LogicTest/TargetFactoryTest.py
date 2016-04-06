from unittest import TestCase
from mock import MagicMock
from Client.BaseStation.Logic.TargetFactory import TargetFactory
from Client.BaseStation.Logic.TargetTypes import *


class TargetFactoryTest(TestCase):

    def test_whenConstructTargetWithShapeJsonThenReturnShapeTarget(self):
        testedFactory = TargetFactory()
        target = testedFactory.constructTarget({"forme":"rectangle"})

        self.assertTrue(isinstance(target, ShapeTarget))

    def test_whenConstructTargetWithColorJsonThenReturnColorTarget(self):
        testedFactory = TargetFactory()
        target = testedFactory.constructTarget({"couleur":"jaune"})

        self.assertTrue(isinstance(target, ColorTarget))