from Client.BaseStation.Logic.Pathfinding.Node import Node

class Obstacle:
    def __init__(self, position):
        self.positionX = position[0]
        self.positionY = position[1]
        self.startingNode = Node((0, 0))

    def setStartingNode(self, node):
        self.startingNode = node
