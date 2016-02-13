import ReferentialConverter

class SpeedCalculator:
    VITESSE = 20 #constante vitesse angulaire, to be updated
    ROTATION_SPEED = 5 #totallement random value!

    def __init__(self):
        self = self

    def generateSpeedInfo(self, pointToMoveTo):
        deplacementRobotX = pointToMoveTo.__getitem__(0)
        deplacementRobotY = pointToMoveTo.__getitem__(1)
        deplacementTotal = deplacementRobotX + deplacementRobotY

        speedX = (deplacementRobotX / deplacementTotal)* self.VITESSE
        speedY = (deplacementRobotY / deplacementTotal)* self.VITESSE

        timeForDeplacement = speedX / deplacementRobotX

        return speedX, speedY, timeForDeplacement