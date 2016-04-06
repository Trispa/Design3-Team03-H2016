from unittest import TestCase
from Client.BaseStation.Logic.Pathfinding.Graph.CollisionDetector import CollisionDetector
from Client.BaseStation.Logic.Pathfinding.Obstacle import Obstacle

class CollisionDetectorTest(TestCase):

    def setUp(self):
        self.anObstacle = Obstacle((100,100))
        self.anObstacleWall = Obstacle((50,50))
        self.anObstacleInner = Obstacle((370,370))
        self.mapSizeX, self.mapSizeY = 1000,600
        safeMargin = 90
        obstacleList = [Obstacle((400,400))]
        self.collisionDetector = CollisionDetector(self.mapSizeX, self.mapSizeY, safeMargin, obstacleList)

    def test_collisionWithEachCorner(self):
        topLeft, topRight, botLeft, botRight = self.collisionDetector.detectCloserObstacleForEachCornerXAxis(self.anObstacle)
        self.assertEqual(topLeft.positionY, 0)
        self.assertEqual(topRight.positionY, 0)
        self.assertEqual(botLeft.positionY, self.mapSizeY)
        self.assertEqual(botRight.positionY, self.mapSizeY)

    def test_collisionWithWall(self):
        wallFront = self.collisionDetector.isCollidingWithWallFront(self.anObstacleWall)
        wallBack = self.collisionDetector.isCollidingWithWallBack(self.anObstacleWall)
        wallTop = self.collisionDetector.isCollidingWithWallUpper(self.anObstacleWall)
        wallBot = self.collisionDetector.isCollidingWithWallLower(self.anObstacleWall)

        self.assertTrue(wallFront)
        self.assertTrue(wallTop)
        self.assertTrue(not wallBack)
        self.assertTrue(not wallBot)

    def test_collisionInnerObstacle(self):
        innerFront = self.collisionDetector.hasFrontalInnerCollision(self.anObstacleInner)
        innerBack = self.collisionDetector.hasEndInnerCollision(self.anObstacleInner)
        innerTop = self.collisionDetector.hasUpperInnerCollision(self.anObstacleInner)
        innerBot = self.collisionDetector.hasLowerInnerCollision(self.anObstacleInner)

        self.assertTrue(not innerFront)
        self.assertTrue(innerTop)
        self.assertTrue(innerBack)
        self.assertTrue(innerBot)