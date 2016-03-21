from Client.BaseStation.Logic.Pathfinding.Obstacle import Obstacle

class CollisionDetector:
    def __init__(self, mapSizeX, mapSizeY, safeMargin, obstacleList):
        self.MAP_SIZE_X = mapSizeX
        self.MAP_SIZE_Y = mapSizeY
        self.SAFE_MARGIN = safeMargin
        self.obstaclesList = obstacleList


    def detectCloserObstacleForEachCornerXAxis(self, verifiedObstacle):
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


    def hasFrontalInnerCollision(self, obstacle):
        for compteur in range(0, self.obstaclesList.__len__()):
            currentObstacle = self.obstaclesList[compteur]
            if currentObstacle != obstacle:
                if currentObstacle.positionY <= obstacle.positionY + 2*self.SAFE_MARGIN and currentObstacle.positionY >= obstacle.positionY - 2*self.SAFE_MARGIN:
                    if currentObstacle.positionX <= obstacle.positionX and currentObstacle.positionX >= obstacle.positionX - 2*self.SAFE_MARGIN:
                        return True
        return False


    def hasEndInnerCollision(self, obstacle):
        for compteur in range(0, self.obstaclesList.__len__()):
            currentObstacle = self.obstaclesList[compteur]
            if currentObstacle != obstacle:
                if currentObstacle.positionY <= obstacle.positionY + 2*self.SAFE_MARGIN and currentObstacle.positionY >= obstacle.positionY - 2*self.SAFE_MARGIN:
                    if currentObstacle.positionX >= obstacle.positionX and currentObstacle.positionX <= obstacle.positionX + 2*self.SAFE_MARGIN:
                        return True
        return False


    def hasUpperInnerCollision(self, obstacle):
        obstacleCollision = []
        result = False
        for compteur in range(0, self.obstaclesList.__len__()):
            currentObstacle = self.obstaclesList[compteur]
            if currentObstacle != obstacle:
                if currentObstacle.positionX <= obstacle.positionX + 2*self.SAFE_MARGIN and currentObstacle.positionX >= obstacle.positionX - 2*self.SAFE_MARGIN:
                    if currentObstacle.positionY < obstacle.positionY and currentObstacle.positionY >= obstacle.positionY - 2*self.SAFE_MARGIN:
                        result = True
                        obstacleCollision.append(currentObstacle)
        return result, obstacleCollision


    def hasLowerInnerCollision(self, obstacle):
        obstacleCollision = []
        result = False
        for compteur in range(0, self.obstaclesList.__len__()):
            currentObstacle = self.obstaclesList[compteur]
            if currentObstacle != obstacle:
                if currentObstacle.positionX <= obstacle.positionX + 2*self.SAFE_MARGIN and currentObstacle.positionX >= obstacle.positionX - 2*self.SAFE_MARGIN:
                    if currentObstacle.positionY > obstacle.positionY and currentObstacle.positionY <= obstacle.positionY + 2*self.SAFE_MARGIN:
                        result = True
                        obstacleCollision.append(currentObstacle)
        return result, obstacleCollision


    def isCollidingWithWallLower(self, obstacle):
        if obstacle.positionY >= self.MAP_SIZE_Y - 2*self.SAFE_MARGIN:
            return True
        return False


    def isCollidingWithWallUpper(self, obstacle):
        if obstacle.positionY <= 0 + 2*self.SAFE_MARGIN:
            return True
        return False


    def isCollidingWithWallFront(self, obstacle):
        if obstacle.positionX <= 0 + 2*self.SAFE_MARGIN:
            return True
        return False


    def isCollidingWithWallBack(self, obstacle):
        if obstacle.positionX >= self.MAP_SIZE_X - 2*self.SAFE_MARGIN:
            return True
        return False