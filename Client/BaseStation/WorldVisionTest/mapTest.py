from unittest import TestCase
from Client.BaseStation.WorldVision.map import Map
from Client.BaseStation.WorldVision.shape import Shape
import numpy as np

class TestMap(TestCase):

    def setUp(self):
        geometricalName = "Square"
        firstContour = np.array([[[1,1], [1,2], [2,2], [2, 1]]], dtype=np.int32)
        secondContour = np.array([[[0,0], [2,3], [3,3], [3, 2]]], dtype=np.int32)
        differentContour = np.array([[[24,32], [34,32], [34,55], [24, 55]]], dtype=np.int32)

        self.firstShape = Shape(geometricalName, firstContour)
        self.secondShape = Shape(geometricalName, secondContour)
        self.differentShape = Shape(geometricalName, differentContour)


    def test_givenAMapContainingOneShapeAndSimilarShapeWhenFindingSimilarShapeInMapWithTheSimilarShapeThenReturnTheShapeContainedInMap(self):
        myMap = Map()
        myMap.addShape(self.firstShape)

        similarShapeInMap = myMap.findSimilarShape(self.secondShape)
        self.assertEqual(self.firstShape, similarShapeInMap)


    def test_givenAMapContainingOneShapeAndADifferentShapeWhenFindingSimilarShapeInMapWithTheDifferentShapeThenReturnNone(self):
        myMap = Map()
        myMap.addShape(self.firstShape)

        similarShapeInMap = myMap.findSimilarShape(self.differentShape)
        self.assertEqual(None, similarShapeInMap)