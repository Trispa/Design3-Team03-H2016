from Client.BaseStation.Logic.Pathfinding.Obstacle import Obstacle
class CollisionDetector:
    def __init__(self, mapSizeX, mapSizeY, safeMargin, obstacleList):
        self.MAP_SIZE_X = mapSizeX
        self.MAP_SIZE_Y = mapSizeY
        self.SAFE_MARGIN = safeMargin
        self.obstaclesList = obstacleList

    def detectStackedObstacleXAxis(self, verifiedObstacle):
        collisionUpperLeftCorner = Obstacle((verifiedObstacle.positionX, 0))
        collisionUpperRightCorner = Obstacle((verifiedObstacle.positionX, 0))
        collisionBottomLeftCorner = Obstacle((verifiedObstacle.positionX, self.MAP_SIZE_Y))
        collisionBottomRightCorner = Obstacle((verifiedObstacle.positionX, self.MAP_SIZE_Y))
        for compteur in range(0, self.obstaclesList.__len__()):
            currentObstacle = self.obstaclesList[compteur]
            if currentObstacle != verifiedObstacle:
                if (verifiedObstacle.positionX - 2*self.SAFE_MARGIN <= currentObstacle.positionX and verifiedObstacle.positionX + 2*self.SAFE_MARGIN >= currentObstacle.positionX):
                    if currentObstacle.positionX <= verifiedObstacle.positionX and currentObstacle.positionY < verifiedObstacle.positionY:
                        if currentObstacle.positionY > collisionUpperLeftCorner.positionY:
                            collisionUpperLeftCorner = currentObstacle
                    if currentObstacle.positionX >= verifiedObstacle.positionX and currentObstacle.positionY < verifiedObstacle.positionY:
                        if currentObstacle.positionY > collisionUpperRightCorner.positionY:
                            collisionUpperRightCorner = currentObstacle
                    if currentObstacle.positionX <= verifiedObstacle.positionX and currentObstacle.positionY > verifiedObstacle.positionY:
                        if currentObstacle.positionY < collisionBottomLeftCorner.positionY:
                            collisionBottomLeftCorner = currentObstacle
                    if currentObstacle.positionX >= verifiedObstacle.positionX and currentObstacle.positionY > verifiedObstacle.positionY:
                        if currentObstacle.positionY < collisionBottomRightCorner.positionY:
                            collisionBottomRightCorner = currentObstacle
        return collisionUpperLeftCorner, collisionUpperRightCorner, collisionBottomLeftCorner, collisionBottomRightCorner