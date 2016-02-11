import time
import ReferentialConverter

class SpeedCalculator:
    VITESSE = 20 #constante vitesse angulaire, to be updated


    def __init__(self, positionRobot, orientation):
        #envoyer une valeur pour identifier le channel de chaque roue
        #self.horizontalWheelFront = WheelMotor(1)
        #self.horizontalWheelBack = WheelMotor(2)
        #self.verticalWheelLeft = WheelMotor(3)
        #self.verticalWheelRight = WheelMotor(4)
        self.referentialConverter = ReferentialConverter(positionRobot, orientation)
        self.isMoving = False


    def moveTo(self, pointToMoveTo):
        self.isMoving = True
        matrixDeplacementRobot = self.referentialConverter.convertWorldToRobot(pointToMoveTo)

        deplacementRobotX = matrixDeplacementRobot.__getitem__(0)
        deplacementRobotY = matrixDeplacementRobot.__getitem__(1)
        deplacementTotal = deplacementRobotX + deplacementRobotY
        speedX = (deplacementRobotX/deplacementTotal)*self.VITESSE
        speedY = (deplacementRobotY/deplacementTotal)*self.VITESSE

        self.__setWheelSpeed(speedX, speedY)

        while deplacementRobotX != 0 and deplacementRobotY != 0: #deplacement not finished
            deplacementRobotY -= speedX
            deplacementRobotY -= speedY
            time.sleep(1) #to be updated

        self.__stopWheel()
        self.isMoving = False


    def setPosition(self, positionRobot, orientation):
        self.referentialConverter.setPosition(positionRobot, orientation)


    def isMoving(self):
        return self.isMoving


    def __stopWheel(self):
        pass
        # self.horizontalWheelFront.setVitesse(0)
        # self.horizontalWheelBack.setVitesse(0)
        # self.verticalWheelLeft.setVitesse(0)
        # self.verticalWheelRight.setVitesse(0)

    def __setWheelSpeed(self, vitesseX, vitesseY):
        pass
        # self.horizontalWheelFront.setVitesse(vitesseX)
        # self.horizontalWheelBack.setVitesse(-vitesseX)
        # self.verticalWheelLeft.setVitesse(vitesseY)
        # self.verticalWheelRight.setVitesse(-vitesseY)
