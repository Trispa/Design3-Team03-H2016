from Client.BaseStation.Logic.Pathfinding.Graph.Node import Node

class SafeZone:
    def __init__(self, cornerTopLeft, cornerTopRight, cornerBottomLeft):
        self.cornerTopLeft = cornerTopLeft
        self.cornerTopRight = cornerTopRight
        self.cornerBottomLeft = cornerBottomLeft
        self.cornerBottomRight = (cornerTopRight[0],cornerBottomLeft[1])
        self.centerNode = Node((0,0))


    def getCenterNodeOfSafeZone(self):
        centerX = (self.cornerTopLeft.__getitem__(0) + self.cornerTopRight.__getitem__(0)) / 2
        centerY = (self.cornerTopLeft.__getitem__(1) + self.cornerBottomLeft.__getitem__(1)) / 2
        centerNode = Node((centerX,centerY))
        self.centerNode = centerNode
        return centerNode