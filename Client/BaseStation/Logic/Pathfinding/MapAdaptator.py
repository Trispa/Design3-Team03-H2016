from Client.BaseStation.Logic.Pathfinding.Obstacle import Obstacle

class MapAdaptator:
    def __init__(self, map):
        self.map = map

    def getMapInfo(self):
        minCorner = (self.map.limit.getMinCorner())
        maxCorner = (self.map.limit.getMaxCorner())
        print minCorner, maxCorner
        mapSizeX = maxCorner[0] - minCorner[0]
        mapSizeY = maxCorner[1] - minCorner[1]
        obstaclesList = []
        for compteur in range(0, self.map.getShapesList().__len__()):
            currentShape = self.map.getShapesList()[compteur]
            centerX, centerY = currentShape.findCenterOfMass()
            obstaclesList.append(Obstacle((centerX - minCorner[0],centerY - minCorner[1])))

        return obstaclesList, mapSizeX, mapSizeY

