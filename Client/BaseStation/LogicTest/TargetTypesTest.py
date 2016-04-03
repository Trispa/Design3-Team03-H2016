from unittest import TestCase
from mock import MagicMock
from Client.BaseStation.Logic.TargetTypes import *
from Client.BaseStation.WorldVision.allShapes import *
from Client.BaseStation.WorldVision.allColors import *


class TargetFactoryTest(TestCase):

    def setUp(self):
        self.blueSquare = Square("Square", np.array([[]], dtype=np.int32))
        self.blueSquare.setColor(GenericColor(np.uint8([[[255,0,0]]]), "Blue"))
        self.redTriangle = Triangle("Triangle", np.array([[]], dtype=np.int32))
        self.redTriangle.setColor(Red(np.uint8([[[150,179,255]]]), "Red"))
        self.obstacleList = [self.blueSquare, self.redTriangle]

    def test_whenInstantiatingColorTargetWithVertThenReturnsColorTargetWithGreenTarget(self):
        testedTarget = ColorTarget("vert")

        self.assertEqual(testedTarget.target, "Green")

    def test_whenInstantiatingColorTargetWithRougeThenReturnsColorTargetWithRedTarget(self):
        testedTarget = ColorTarget("rouge")

        self.assertEqual(testedTarget.target, "Red")

    def test_whenInstantiatingColorTargetWithBleuThenReturnsColorTargetWithBlueTarget(self):
        testedTarget = ColorTarget("bleu")

        self.assertEqual(testedTarget.target, "Blue")

    def test_whenInstantiatingColorTargetWithJauneThenReturnsColorTargetWithYellowTarget(self):
        testedTarget = ColorTarget("jaune")

        self.assertEqual(testedTarget.target, "Yellow")

    def test_whenInstantiatingShapeTargetWithRectangleThenReturnsShapeTargetWithSquareTarget(self):
        testedTarget = ShapeTarget("rectangle")

        self.assertEqual(testedTarget.target, "Square")

    def test_whenInstantiatingShapeTargetWithTriangleThenReturnsShapeTargetWithTriangleTarget(self):
        testedTarget = ShapeTarget("triangle")

        self.assertEqual(testedTarget.target, "Triangle")

    def test_whenInstantiatingShapeTargetWithCercleThenReturnsShapeTargetWithCircleTarget(self):
        testedTarget = ShapeTarget("cercle")

        self.assertEqual(testedTarget.target, "Circle")

    def test_whenInstantiatingShapeTargetWithPentagoneThenReturnsShapeTargetWithPentagoneTarget(self):
        testedTarget = ShapeTarget("pentagone")

        self.assertEqual(testedTarget.target, "Pentagone")

    def test_whenGetObstacleOnShapeTargetThenReturnsCorrectObstacleWithTarget(self):
        testedTarget = ShapeTarget("rectangle")
        obstacle = testedTarget.getObstacle(self.obstacleList)

        self.assertEqual(obstacle.getName(), self.obstacleList[0].getName())

    def test_whenGetObstacleOnColorTargetThenReturnsCorrectObstacleWithTarget(self):
        testedTarget = ColorTarget("rouge")
        obstacle = testedTarget.getObstacle(self.obstacleList)

        self.assertEqual(obstacle.getName(), self.obstacleList[1].getName())

