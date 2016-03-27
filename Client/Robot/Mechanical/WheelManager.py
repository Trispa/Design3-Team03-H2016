import time
import SerialPortCommunicator
from threading import Timer,Thread,Event



class MoteurRoue:
    NB_MOTEUR = 5
    CW = 0
    CCW = 1
    X_AXIS = 0
    Y_AXIS = 1
    POSITIVE_SPEED = 1
    NEGATIVE_SPEED = 0

    def __init__(self):
        self.spc = SerialPortCommunicator.SerialPortCommunicator()
        self.thread = None
        self.isRunning = False
        self.MAX_SPEED = 0.14

    def stopAllMotors(self):
        self.spc.stopAllMotor()
        self.isRunning = False

    def stopAllMotorsInterrupt(self):
        self.spc.stopAllMotor()
        self.isRunning = False
        self.thread.cancel()

    def rotation(self, degree):
        # while self.isRunning:
        #     pass
        self.isRunning = True
        speed = 0.05
        timeToSleep = 0.035 * abs(degree) + 0.075
        direction = "CW"
        if degree <= 0:
            direction = "CCW"


        self.beforeChangeDirection()
        if(direction == 'CW'):
            self.spc.driveMoteurRotation(speed, 0)
            # for i in range(1, NB_MOTEUR):
            #     self.spc.driveMoteur(i, speed, CW)
            #     # time.sleep(0.01)
        elif(direction == "CCW"):
            self.spc.driveMoteurRotation(speed, 1)
            # for i in range(1, NB_MOTEUR):
            #     self.spc.driveMoteur(i, speed, CCW)

        time.sleep(timeToSleep)
        self.stopAllMotors()
        # self.debutDeLInterruption(timeToSleep)
        return timeToSleep


    def beforeChangeDirection(self):
        self.stopAllMotors()
        time.sleep(0.2)

    def debutDeLInterruption(self, t):
        self.thread = Timer(t, self.stopAllMotorsInterrupt)
        self.thread.start()

#Distance en centimetre
    def avanceVector(self, x, y):
        # while self.isRunning:
        #     pass
        self.isRunning = True
        self.beforeChangeDirection()
        xSpeed = self.MAX_SPEED
        ySpeed = self.MAX_SPEED
        if abs(x) > abs(y):
            ySpeed = (abs(y) * xSpeed) / abs(x)
        elif abs(x) < abs(y):
            xSpeed = (abs(x) * ySpeed) / abs(y)

        timeToTravel = max(abs(x), abs(y)) / (max(xSpeed, ySpeed) * 100) + max(xSpeed, ySpeed) * 1.1

        print("xSpeed : " + str(xSpeed) + " ySpeed : " + str(ySpeed) + " Time : " + str(timeToTravel))

        #positif 1
        #negatif 0
        #axe x = 0
        #axe y = 1
        if x > 0:
            self.spc.driveMoteurLine(self.X_AXIS, xSpeed, self.POSITIVE_SPEED)
        if x < 0:
            self.spc.driveMoteurLine(self.X_AXIS, xSpeed, self.NEGATIVE_SPEED)
        if y > 0:
            self.spc.driveMoteurLine(self.Y_AXIS, ySpeed, self.POSITIVE_SPEED)
        if y < 0:
            self.spc.driveMoteurLine(self.Y_AXIS, ySpeed, self.NEGATIVE_SPEED)

        # self.debutDeLInterruption(timeToTravel)
        time.sleep(timeToTravel)
        self.stopAllMotors()
        return timeToTravel



    def isRunning(self):
        return self.isRunning


    def demo3(self):
        self.avanceVector(0, 66)
        time.sleep(0.5)
        self.avanceVector(-66, 0)
        time.sleep(0.5)
        self.avanceVector(0, -66)
        time.sleep(0.5)
        self.avanceVector(66, 0)
        time.sleep(0.5)
        self.avanceVector(-50, -50)
        time.sleep(0.5)
        self.avanceVector(50, 50)

    def demoR(self):
        self.rotation("CW", 180)
        time.sleep(1)
        self.rotation("CCW", 90)
        time.sleep(1)
        self.rotation("CW", 90)
        time.sleep(1)
        self.rotation("CCW", 180)



if __name__ == '__main__':
    mr = MoteurRoue()
    mr.stopAllMotors()
    time.sleep(0.1)

    mr.avanceVector(-30, 0)
    time.sleep(2)
    mr.avanceVector(30, 0)
    # mr.avanceVector(10, 0)
    # mr.avanceVector(0, 10)
    # mr.avanceVector(0, -10)
    # mr.rotation(-90)
    # mr.rotation(90)



