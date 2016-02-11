import ReferentialConverter

class SpeedCalculator:
    VITESSE = 20 #constante vitesse angulaire, to be updated

    def __init__(self, positionRobot, orientation):
        self.referentialConverter = ReferentialConverter(positionRobot, orientation)


    def generateSpeedInfo(self, pointToMoveTo):
        matrixDeplacementRobot = self.referentialConverter.convertWorldToRobot(pointToMoveTo)
        return self.__transformCoordinatesToSpeed(matrixDeplacementRobot)


    def __transformCoordinatesToSpeed(self, matrixDeplacementRobot):
        deplacementRobotX = matrixDeplacementRobot.__getitem__(0)
        deplacementRobotY = matrixDeplacementRobot.__getitem__(1)
        deplacementTotal = deplacementRobotX + deplacementRobotY

        speedX = (deplacementRobotX / deplacementTotal)* self.VITESSE
        speedY = (deplacementRobotY / deplacementTotal)* self.VITESSE

        timeForDeplacement = speedX / deplacementRobotX

        return speedX, speedY, timeForDeplacement