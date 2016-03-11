from Client.BaseStation.Logic.Pathfinding.Obstacle import Obstacle

class MapAdaptator:
    def __init__(self, map):
        self.map = map

    def getObstaclesList(self):
        obstaclesList = []
        for compteur in range(0, self.map.shapes.__len__()):
            currentShape = map.shapes[compteur]
            centerX, centerY = currentShape.findCenterOfMass()
            obstaclesList.append(Obstacle((centerX,centerY)))
        return obstaclesList

