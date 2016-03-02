import time
from SpeedCalculator import SpeedCalculator
import sys


class WheelManager:
    def __init__(self, moteurRoue):
        #envoyer une valeur pour identifier le channel de chaque roue

        self.moteurRoue = moteurRoue
        self.speedCalculator = SpeedCalculator()
        self.isMoving = False


    def moveTo(self, pointToMoveTo):

            self.isMoving = True
            timeToTravel = self.moteurRoue.avanceVector(pointToMoveTo[0],pointToMoveTo[1])
            self.isMoving = False


    def rotate(self, angle):
        angle = angle%360
        if angle != 0 :
            self.isMoving = True
            rotationSpeed, timeForRotation = self.speedCalculator.generateRotationInfos(angle)

            self.moteurRoue.rotation(angle)


            self.isMoving = False


    def isMoving(self):
        return self.isMoving



    def __pointNotNull(self, pointToVerify):
        return (pointToVerify.__getitem__(0) != 0 or pointToVerify.__getitem__(1) != 0)

