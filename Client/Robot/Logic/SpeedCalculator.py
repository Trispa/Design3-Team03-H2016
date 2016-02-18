import ReferentialConverter

class SpeedCalculator:
    VITESSE = 20 #constante vitesse angulaire, to be updated
    ROTATION_SPEED = 5 #totallement random value!
    TIME_FOR_A_360 = 10 #not

    def __init__(self):
        self = self

    def generateSpeedInfos(self, pointToMoveTo):
        if (pointToMoveTo.__getitem__(0) == 0 and pointToMoveTo.__getitem__(1) == 0):
            speedX = 0
            speedY = 0
            timeForDeplacement = 0

        else:
            deplacementRobotX = pointToMoveTo.__getitem__(0)
            deplacementRobotY = pointToMoveTo.__getitem__(1)
            deplacementTotal = float(deplacementRobotX + deplacementRobotY)

            speedX = (deplacementRobotX / deplacementTotal)* self.VITESSE
            speedY = (deplacementRobotY / deplacementTotal)* self.VITESSE

            timeForDeplacement = deplacementRobotX / speedX

        return speedX, speedY, timeForDeplacement


    def generateRotationInfos(self, angle):
        timeForTheRotation = float(angle)/360*self.TIME_FOR_A_360
        return self.ROTATION_SPEED, timeForTheRotation
