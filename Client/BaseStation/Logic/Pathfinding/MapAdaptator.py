from Client.BaseStation.Logic.Pathfinding.Obstacle import Obstacle

class MapAdaptator:
    def __init__(self, map):
        self.map = map

    def getMapInfo(self):

        limit = self.map.getMapLimit()
        minCorner = (limit.getMinCorner())
        maxCorner = (limit.getMaxCorner())
        mapSizeX = maxCorner[0] - minCorner[0]
        mapSizeY = maxCorner[1] - minCorner[1]

        obstaclesList = []
        self.map.getShapesList().sort(key=lambda shape: shape.findCenterOfMass()[0])
        for compteur in range(0, self.map.getShapesList().__len__()):
            currentShape = self.map.getShapesList()[compteur]

            centerX, centerY = currentShape.findCenterOfMass()
            if centerY > minCorner[1] and centerY < maxCorner[1]:
                if obstaclesList.__len__() > 0:
                    if centerX-minCorner[0] == obstaclesList[compteur-1].positionX:
                        centerX += 1
                    elif centerX-minCorner[0] < obstaclesList[compteur-1].positionX:
                        centerX += 2
                obstaclesList.append(Obstacle((centerX - minCorner[0],centerY - minCorner[1])))
        return obstaclesList, mapSizeX, mapSizeY, minCorner

