class MapCoordinatesAjuster:
    def __init__(self, map):
        limit = map.getMapLimit()
        self.minCorner = limit.getMinCorner()

    def convertPoint(self, pointToBeConverted):
        return (pointToBeConverted[0] - self.minCorner[0], pointToBeConverted[1] - self.minCorner[1])
