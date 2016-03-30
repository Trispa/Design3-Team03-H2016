class MapCoordinatesAjuster:
    def __init__(self, map):
        self.minCorner = map.limit.getMinCorner()

    def convertPoint(self, pointToBeConverted):
        return (pointToBeConverted[0] - self.minCorner[0], pointToBeConverted[1] - self.minCorner[1])

    def inverseConversion(self, pointToBeConverted):
        return (pointToBeConverted[0] + self.minCorner[0], pointToBeConverted[1] + self.minCorner[1])