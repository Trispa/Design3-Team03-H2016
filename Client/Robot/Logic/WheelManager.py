import time
import SpeedCalculator
from Client.Robot.Mechanical.WheelMotor import WheelMotor

class WheelManager:
    def __init__(self, positionRobot, orientation):
        #envoyer une valeur pour identifier le channel de chaque roue
        self.horizontalWheelFront = WheelMotor(1)
        self.horizontalWheelBack = WheelMotor(2)
        self.verticalWheelLeft = WheelMotor(3)
        self.verticalWheelRight = WheelMotor(4)

        self.speedCalculator = SpeedCalculator(positionRobot, orientation)
        self.isMoving = False


    def moveTo(self, pointToMoveTo):
        self.isMoving = True
        speedX, speedY, timeForDeplacement = self.speedCalculator.generateSpeedInfo(pointToMoveTo)
        self.__setWheelSpeed(speedX, speedY)
        time.sleep(timeForDeplacement)
        self.__stopWheel()
        self.isMoving = False


    def rotate(self, angle):
        angle = angle%360
        self.horizontalWheelFront.setVitesse(self.speedCalculator.ROTATION_SPEED)
        self.horizontalWheelBack.setVitesse(self.speedCalculator.ROTATION_SPEED)
        self.verticalWheelLeft.setVitesse(self.speedCalculator.ROTATION_SPEED)
        self.verticalWheelRight.setVitesse(self.speedCalculator.ROTATION_SPEED)

        timeNeededToDoTheRotation = 5*float(angle/360) # 5 = temps pour effectuer un 360 != vraiment 5!!!!
        time.sleep(timeNeededToDoTheRotation)
        self.__stopWheel()


    def setPosition(self, positionRobot, orientation):
        self.referentialConverter.setPosition(positionRobot, orientation)


    def isMoving(self):
        return self.isMoving


    def __stopWheel(self):
        self.horizontalWheelFront.setVitesse(0)
        self.horizontalWheelBack.setVitesse(0)
        self.verticalWheelLeft.setVitesse(0)
        self.verticalWheelRight.setVitesse(0)


    def __setWheelSpeed(self, vitesseX, vitesseY):
        self.horizontalWheelFront.setVitesse(vitesseX)
        self.horizontalWheelBack.setVitesse(-vitesseX)
        self.verticalWheelLeft.setVitesse(vitesseY)
        self.verticalWheelRight.setVitesse(-vitesseY)
