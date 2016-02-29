import time
from Client.Robot.Logic.SpeedCalculator import SpeedCalculator
from Client.Robot.Mechanical.WheelMotor import WheelMotor
from Client.Robot.Mechanical.MoteurRoue import MoteurRoue

class WheelManager:
    def __init__(self,horizontalWheelFront, horizontalWheelBack, verticalWheelLeft, verticalWheelRight):
        #envoyer une valeur pour identifier le channel de chaque roue
        self.horizontalWheelFront = horizontalWheelFront
        self.horizontalWheelBack = horizontalWheelBack
        self.verticalWheelLeft = verticalWheelLeft
        self.verticalWheelRight = verticalWheelRight
        self.moteurRoue = MoteurRoue()
        self.speedCalculator = SpeedCalculator()
        self.isMoving = False


    def moveTo(self, pointToMoveTo):

            self.isMoving = True
            timeToTravel = self.moteurRoue.avanceVector(pointToMoveTo[0],pointToMoveTo[1])
            time.sleep(timeToTravel)
            self.isMoving = False


    def rotate(self, angle):
        angle = angle%360
        if angle != 0 :
            self.isMoving = True
            rotationSpeed, timeForRotation = self.speedCalculator.generateRotationInfos(angle)

            self.horizontalWheelFront.setVitesse(rotationSpeed)
            self.horizontalWheelBack.setVitesse(rotationSpeed)
            self.verticalWheelLeft.setVitesse(rotationSpeed)
            self.verticalWheelRight.setVitesse(rotationSpeed)

            time.sleep(timeForRotation)

            self.__stopWheel()
            self.isMoving = False


    def isMoving(self):
        return self.isMoving


    def __stopWheel(self):
        self.horizontalWheelFront.setVitesse(0)
        self.horizontalWheelBack.setVitesse(0)
        self.verticalWheelLeft.setVitesse(0)
        self.verticalWheelRight.setVitesse(0)


    def __setWheelDeplacementSpeed(self, vitesseX, vitesseY):
        self.horizontalWheelFront.setVitesse(vitesseX)
        self.horizontalWheelBack.setVitesse(-vitesseX)
        self.verticalWheelLeft.setVitesse(vitesseY)
        self.verticalWheelRight.setVitesse(-vitesseY)


    def __pointNotNull(self, pointToVerify):
        return (pointToVerify.__getitem__(0) != 0 or pointToVerify.__getitem__(1) != 0)

