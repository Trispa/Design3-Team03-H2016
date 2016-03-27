import time
import SerialPortCommunicator
from Client.Robot.Logic.Deplacement.PixelToCentimeterConverter import PixelToCentimeterConverter

from threading import Timer,Thread,Event

class MoteurRoue:
    NB_MOTEUR = 5
    CW = 0
    CCW = 1
    X_AXIS = 0
    Y_AXIS = 1
    POSITIVE_SPEED = 1
    NEGATIVE_SPEED = 0
    MAX_SPEED = 0.14
    ROTATION_SPEED = 0,05

    def __init__(self):
        self.spc = SerialPortCommunicator.SerialPortCommunicator()
        self.pixelToCentimeterConverter = PixelToCentimeterConverter()
        self.thread = None
        self.isMoving = False

    #Distance en pixel
    def moveTo(self, pointToMoveTo):
        pointConverted = self.pixelToCentimeterConverter.convertPixelToCentimeter(pointToMoveTo)
        pointX = pointConverted[0]
        pointY = pointConverted[1]

        self.isMoving = True
        self.__resetMotors()
        xSpeed = self.MAX_SPEED
        ySpeed = self.MAX_SPEED

        if abs(pointX) > abs(pointY):
            ySpeed = (abs(pointY) * xSpeed) / abs(pointX)
        elif abs(pointX) < abs(pointY):
            xSpeed = (abs(pointX) * ySpeed) / abs(pointY)

        timeToTravel = max(abs(pointX), abs(pointY)) / (max(xSpeed, ySpeed) * 100) + max(xSpeed, ySpeed) * 1.1
        print("xSpeed : " + str(xSpeed) + " ySpeed : " + str(ySpeed) + " Time : " + str(timeToTravel))

        if pointX > 0:
            self.spc.driveMoteurLine(self.X_AXIS, xSpeed, self.POSITIVE_SPEED)
        if pointX < 0:
            self.spc.driveMoteurLine(self.X_AXIS, xSpeed, self.NEGATIVE_SPEED)
        if pointY > 0:
            self.spc.driveMoteurLine(self.Y_AXIS, ySpeed, self.POSITIVE_SPEED)
        if pointY < 0:
            self.spc.driveMoteurLine(self.Y_AXIS, ySpeed, self.NEGATIVE_SPEED)

        # self.debutDeLInterruption(timeToTravel)
        time.sleep(timeToTravel)
        self.__stopAllMotors()
        return timeToTravel


    def rotate(self, degree):
        # while self.isRunning:
        #     pass
        self.isMoving = True
        timeToSleep = 0.035 * abs(degree) + 0.075
        self.__resetMotors()

        if(degree <= 0):
            self.spc.driveMoteurRotation(self.ROTATION_SPEED, self.NEGATIVE_SPEED)
        else:
            self.spc.driveMoteurRotation(self.ROTATION_SPEED, self.POSITIVE_SPEED)
        time.sleep(timeToSleep)
        # self.debutDeLInterruption(timeToSleep)
        self.__stopAllMotors()
        return timeToSleep


    def isRunning(self):
        return self.isMoving

    def __resetMotors(self):
        self.__stopAllMotors()
        time.sleep(0.2)

    def __debutDeLInterruption(self, timeToWait):
        self.thread = Timer(timeToWait, self.__stopAllMotorsInterrupt)
        self.thread.start()

    def __stopAllMotors(self):
        self.spc.stopAllMotor()
        self.isMoving = False

    def __stopAllMotorsInterrupt(self):
        self.spc.stopAllMotor()
        self.isMoving = False
        self.thread.cancel()


    def demo3(self):
        self.moveTo(0, 66)
        time.sleep(0.5)
        self.moveTo(-66, 0)
        time.sleep(0.5)
        self.moveTo(0, -66)
        time.sleep(0.5)
        self.moveTo(66, 0)
        time.sleep(0.5)
        self.moveTo(-50, -50)
        time.sleep(0.5)
        self.moveTo(50, 50)

    def demoR(self):
        self.rotate("CW", 180)
        time.sleep(1)
        self.rotate("CCW", 90)
        time.sleep(1)
        self.rotate("CW", 90)
        time.sleep(1)
        self.rotate("CCW", 180)



if __name__ == '__main__':
    mr = MoteurRoue()
    mr.__stopAllMotors()
    time.sleep(0.1)

    mr.moveTo(-30, 0)
    time.sleep(2)
    mr.moveTo(30, 0)
    # mr.avanceVector(10, 0)
    # mr.avanceVector(0, 10)
    # mr.avanceVector(0, -10)
    # mr.rotation(-90)
    # mr.rotation(90)



