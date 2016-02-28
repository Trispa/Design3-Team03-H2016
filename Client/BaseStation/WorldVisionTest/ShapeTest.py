from unittest import TestCase
from Client.BaseStation.WorldVision.shape import Shape
import numpy as np


class TestShape(TestCase):

    def test_givenTwoShapesWithSameContourWhenComparedThenTheyAreEqual(self):
        myContour = np.array([[1,1],[10,50],[50,50]], dtype=np.int32)
        aGeometricalName = "Triangle"
        myFirstShape = Shape(aGeometricalName, myContour)
        mySecondShape = Shape(aGeometricalName, myContour)
        self.assertTrue(myFirstShape == mySecondShape)

    def test_givenTwoShapesWithDifferentContourWhenComparedThenTheyAreNotEqual(self):
        myFirstContour = np.array([[1,1],[10,50],[50,50]], dtype=np.int32)
        mySecondContour = np.array([[1,2],[10,51],[50,52]], dtype=np.int32)
        aGeometricalName = "Triangle"
        myFirstShape = Shape(aGeometricalName, myFirstContour)
        mySecondShape = Shape(aGeometricalName, mySecondContour)
        self.assertFalse(myFirstShape == mySecondShape)

    def test_givenTwoShapeWithOneNotIniTializeWhenComparedThenTheyAreNotEqual(self):
        myFirstContour = np.array([[1,1],[10,50],[50,50]], dtype=np.int32)
        aGeometricalName = "Triangle"
        myFirstShape = Shape(aGeometricalName, myFirstContour)
        mySecondShape = None
        self.assertFalse(myFirstShape == mySecondShape)

    def test_givenAShapeWithSimilarLenghtEdgesWhenIsEqualEdgesThenEdgesAreEquals(self):
        squareContour = np.array([[0,0], [0,1], [1,0], [1,1]], dtype=np.int32)
        aGeometricalName = "Triangle"
        myShape = Shape(aGeometricalName, squareContour)
        self.assertTrue(myShape.isEqualEdges())

    def test_givenAShapeWithDifferentLenghtEdgesWhenIsEqualEdgesThenEdgesAreNotEquals(self):
        squareContour = np.array([[0,0], [0,1], [1,30]], dtype=np.int32)
        aGeometricalName = "Triangle"
        myShape = Shape(aGeometricalName, squareContour)
        self.assertFalse(myShape.isEqualEdges())

