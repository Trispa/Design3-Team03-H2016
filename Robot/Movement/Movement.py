class Mouvement:
    positionWorldX = 0
    positionWorldY = 0

    def __init__(self, positionRobotX, positionRobotY):
        self.positionWorldX = positionRobotX
        self.positionWorldY = positionRobotY

    def moveTo(self, pointToMoveTo):
        distanceX = self.positionWorldX - pointToMoveTo


    def setPosition(self, positionX, positionY):
        self.positionWorldX = positionX
        self.positionWorldY = positionY

