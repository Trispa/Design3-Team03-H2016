import time
import SerialPortCommunicator
from threading import Timer,Thread,Event

NB_MOTEUR = 5
CW = 0
CCW = 1
MAX_SPEED = 0.15
class MoteurRoue:
    def __init__(self):
        self.spc = SerialPortCommunicator.SerialPortCommunicator()
        self.thread = None
        self.isRunning = False

    def stopAllMotors(self):
        self.spc.stopAllMotor()

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
            for i in range(1, NB_MOTEUR):
                self.spc.driveMoteur(i, speed, CW)
                # time.sleep(0.01)
        elif(direction == "CCW"):
            for i in range(1, NB_MOTEUR):
                self.spc.driveMoteur(i, speed, CCW)
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
        xSpeed = MAX_SPEED
        ySpeed = MAX_SPEED
        if abs(x) > abs(y):
            ySpeed = (abs(y) * xSpeed) / abs(x)
        elif abs(x) < abs(y):
            xSpeed = (abs(x) * ySpeed) / abs(y)

        timeToTravel = max(abs(x), abs(y)) / (max(xSpeed, ySpeed) * 100)

        print("xSpeed : " + str(xSpeed) + " ySpeed : " + str(ySpeed) + " Time : " + str(timeToTravel))

        if x > 0:
            self.spc.driveMoteur(3, xSpeed, CCW)
            self.spc.driveMoteur(2, xSpeed, CW)
        if x < 0:
            self.spc.driveMoteur(3, xSpeed, CW)
            self.spc.driveMoteur(2, xSpeed, CCW)
        if y > 0:
            self.spc.driveMoteur(1, ySpeed, CCW)
            self.spc.driveMoteur(4, ySpeed, CW)
        if y < 0:
            self.spc.driveMoteur(1, ySpeed, CW)
            self.spc.driveMoteur(4, ySpeed, CCW)

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




