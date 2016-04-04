import time
from threading import Timer

import numpy as np

import Client.Robot.Mechanical.SerialPortCommunicator
from Client.Robot.Movement.PixelToCentimeterConverter import PixelToCentimeterConverter
from Client.Robot.Logic.ReferentialConverter import ReferentialConverter


class WheelManager:
    NB_MOTEUR = 5
    CW = 0
    CCW = 1
    X_AXIS = 0
    Y_AXIS = 1
    POSITIVE_SPEED = 1
    NEGATIVE_SPEED = 0
    MAX_SPEED = 0.11
    MAX_SPEED_VISION = 0.03
    ROTATION_SPEED = 0.05

    def __init__(self, serialPortCommunicator):
        self.spc = serialPortCommunicator
        self.pixelToCentimeterConverter = PixelToCentimeterConverter()
        self.thread = None
        self.isMoving = False

    #Distance en pixel
    def moveTo(self, pointToMoveTo):
        print pointToMoveTo[0], pointToMoveTo[1], "point.fsd"
        if not(pointToMoveTo[0] == 0 or pointToMoveTo[1] == 0):
            pointAdjusted = self.__adjustOrientation(pointToMoveTo)
        else:
            pointAdjusted = pointToMoveTo

        pointConverted = self.pixelToCentimeterConverter.convertPixelToCentimeter(pointAdjusted)


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
        self.stopAllMotors()
        return timeToTravel

    def moveForever(self, pointX, pointY):

        self.isMoving = True
        self.__resetMotors()
        xSpeed = self.MAX_SPEED_VISION
        ySpeed = self.MAX_SPEED_VISION

        if abs(pointX) > abs(pointY):
            ySpeed = (abs(pointY) * xSpeed) / abs(pointX)
        elif abs(pointX) < abs(pointY):
            xSpeed = (abs(pointX) * ySpeed) / abs(pointY)


        print("xSpeed : " + str(xSpeed) + " ySpeed : " + str(ySpeed))

        if pointX > 0:
            self.spc.driveMoteurLine(self.X_AXIS, xSpeed, self.POSITIVE_SPEED)
        if pointX < 0:
            self.spc.driveMoteurLine(self.X_AXIS, xSpeed, self.NEGATIVE_SPEED)
        if pointY > 0:
            self.spc.driveMoteurLine(self.Y_AXIS, ySpeed, self.POSITIVE_SPEED)
        if pointY < 0:
            self.spc.driveMoteurLine(self.Y_AXIS, ySpeed, self.NEGATIVE_SPEED)

        # self.debutDeLInterruption(timeToTravel)



    def rotate(self, degree):
        self.isMoving = True
        timeToSleep = 0.029 * abs(degree) + 0.145
        self.__resetMotors()

        if(degree <=0):
            self.spc.driveMoteurRotation(self.ROTATION_SPEED, self.NEGATIVE_SPEED)
        else:
            self.spc.driveMoteurRotation(self.ROTATION_SPEED, self.POSITIVE_SPEED)
        print timeToSleep
        time.sleep(timeToSleep)
        # self.debutDeLInterruption(timeToSleep)
        self.stopAllMotors()
        return timeToSleep


    def setOrientation(self, currentRobotOrientation, angleToSet):
        if (angleToSet - currentRobotOrientation < 0 and angleToSet - currentRobotOrientation <= -180):
            angleToSet += 360
            angleToRotate = -(angleToSet - currentRobotOrientation)
        elif (angleToSet - currentRobotOrientation < 0 and angleToSet - currentRobotOrientation > -180):
            angleToRotate = -(currentRobotOrientation - angleToSet)
        elif (angleToSet - currentRobotOrientation < 180):
            angleToRotate = angleToSet - currentRobotOrientation
        else:
            angleToRotate = angleToSet - (currentRobotOrientation+360)
        print angleToRotate
        self.rotate(-angleToRotate)


    def isRunning(self):
        return self.isMoving


    def __adjustOrientation(self, pointToMove):
        degreeAngle = (np.arctan((pointToMove[1]/pointToMove[0]))/np.pi)*180
        angleToRotate = degreeAngle%45
        print angleToRotate
        point = (0,0)
        referentialConverter = ReferentialConverter(point, angleToRotate)

        self.rotate(-angleToRotate)

        pointAdjusted = referentialConverter.convertWorldToRobot(pointToMove)
        print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ BOBA FETT", pointAdjusted[0], pointAdjusted[1]
        return pointAdjusted


    def __resetMotors(self):
        self.stopAllMotors()
        time.sleep(0.2)

    def __interruptionStart(self, timeToWait):
        self.thread = Timer(timeToWait, self.__stopAllMotorsFromInterruption)
        self.thread.start()

    def stopAllMotors(self):
        self.spc.stopAllMotor()
        self.isMoving = False

    def __stopAllMotorsFromInterruption(self):
        self.spc.stopAllMotor()
        self.isMoving = False
        self.thread.cancel()


    # def demo3(self):
    #     self.moveTo(0, 66)
    #     time.sleep(0.5)
    #     self.moveTo(-66, 0)
    #     time.sleep(0.5)
    #     self.moveTo(0, -66)
    #     time.sleep(0.5)
    #     self.moveTo(66, 0)
    #     time.sleep(0.5)
    #     self.moveTo(-50, -50)
    #     time.sleep(0.5)
    #     self.moveTo(50, 50)
    #
    #
    # def demoR(self):
    #     self.rotate("CW", 180)
    #     time.sleep(1)
    #     self.rotate("CCW", 90)
    #     time.sleep(1)
    #     self.rotate("CW", 90)
    #     time.sleep(1)
    #     self.rotate("CCW", 180)


if __name__ == '__main__':
    pass
    # mr = WheelManager()
    # mr.stopAllMotors()
    # time.sleep(0.1)
    #
    # mr.moveTo((0, 50))
    # time.sleep(2)
    # mr.moveTo((0, -50))
    # time.sleep(2)
    # mr.moveTo((50, 0))
    # time.sleep(2)
    # mr.moveTo((-50, 0))
    # mr.avanceVector(10, 0)
    # mr.avanceVector(0, 10)
    # mr.avanceVector(0, -10)
    # mr.rotation(-90)
    # mr.rotation(90)



