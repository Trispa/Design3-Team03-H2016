import time
from threading import Timer

import numpy as np

from Client.Robot.Mechanical.SerialPortCommunicator import SerialPortCommunicator
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
    MAX_SPEED_VISION = 0.02
    ROTATION_SPEED = 0.04

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

        timeToTravel = max(abs(pointX), abs(pointY)) / (max(xSpeed, ySpeed) * 100) + max(xSpeed, ySpeed)
        timeToTravel = timeToTravel * 1.03
        print("xSpeed : " + str(xSpeed) + " ySpeed : " + str(ySpeed) + " Time : " + str(timeToTravel))
        print "Reel d   istance : ", xSpeed * timeToTravel

        distanceCm = max(abs(pointConverted[0]), abs(pointConverted[1]))

        if pointX > 0:
            self.spc.driveMoteurLine(self.X_AXIS, xSpeed, self.POSITIVE_SPEED, distanceCm)
        if pointX < 0:
            self.spc.driveMoteurLine(self.X_AXIS, xSpeed, self.NEGATIVE_SPEED, distanceCm)
        if pointY > 0:
            self.spc.driveMoteurLine(self.Y_AXIS, ySpeed, self.POSITIVE_SPEED, distanceCm)
        if pointY < 0:
            self.spc.driveMoteurLine(self.Y_AXIS, ySpeed, self.NEGATIVE_SPEED, distanceCm)

        # self.debutDeLInterruption(timeToTravel)
        time.sleep(timeToTravel)
        self.stopAllMotors()
        return timeToTravel

    def moveForever(self, pointX, pointY):

        self.isMoving = True
        xSpeed = self.MAX_SPEED_VISION
        ySpeed = self.MAX_SPEED_VISION

        if abs(pointX) > abs(pointY):
            ySpeed = (abs(pointY) * xSpeed) / abs(pointX)
        elif abs(pointX) < abs(pointY):
            xSpeed = (abs(pointX) * ySpeed) / abs(pointY)



        if pointX > 0:
            self.spc.driveMoteurLinePrecision(self.X_AXIS, xSpeed, self.POSITIVE_SPEED, 100)
        if pointX < 0:
            self.spc.driveMoteurLinePrecision(self.X_AXIS, xSpeed, self.NEGATIVE_SPEED, 100)
        if pointY > 0:
            self.spc.driveMoteurLinePrecision(self.Y_AXIS, ySpeed, self.POSITIVE_SPEED, 100)
        if pointY < 0:
            self.spc.driveMoteurLinePrecision(self.Y_AXIS, ySpeed, self.NEGATIVE_SPEED, 100)


        # self.debutDeLInterruption(timeToTravel)



    def rotate(self, degree):
        self.isMoving = True
        timeToSleep = 0.035 * abs(degree) + 0.168
        self.__resetMotors()
        print "rotating", degree
        if(degree <=0):
            self.spc.driveMoteurRotation(self.ROTATION_SPEED, self.NEGATIVE_SPEED, abs(degree))
        else:
            self.spc.driveMoteurRotation(self.ROTATION_SPEED, self.POSITIVE_SPEED, abs(degree))
        print timeToSleep
        time.sleep(timeToSleep+1)
        # self.debutDeLInterruption(timeToSleep)
        # self.stopAllMotors()
        return timeToSleep


    def setOrientation(self, currentRobotOrientation, angleToSet):
        print currentRobotOrientation, "<= robot", angleToSet, "<= setting"
        if (angleToSet - currentRobotOrientation < 0 and angleToSet - currentRobotOrientation <= -180):
            angleToSet += 360
            angleToRotate = angleToSet - currentRobotOrientation
        elif (angleToSet - currentRobotOrientation < 0 and angleToSet - currentRobotOrientation > -180):
            angleToRotate = -(currentRobotOrientation - angleToSet)
            print "boba2"
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
        angleToRotate = degreeAngle%90
        print angleToRotate
        point = (0,0)
        referentialConverter = ReferentialConverter(point, angleToRotate)
        print "adjusting angle", -angleToRotate
        self.rotate(-angleToRotate)

        pointAdjusted = referentialConverter.convertWorldToRobot(pointToMove)
        print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ BOBA FETT", pointAdjusted[0], pointAdjusted[1]
        return pointAdjusted


    def __resetMotors(self):
        self.stopAllMotors()

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
    ratio = 49/9.5
    spc = SerialPortCommunicator()
    mr = WheelManager(spc)
    mr.stopAllMotors()
    time.sleep(0.1)

    mr.moveTo((19*ratio, 0))


    # mr.rotate(20)
    # time.sleep(3)
    # mr.rotate(20)
    # time.sleep(3)
    # mr.rotate(40)
    # time.sleep(3)
    # mr.rotate(10)



