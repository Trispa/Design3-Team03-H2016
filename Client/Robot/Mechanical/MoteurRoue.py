import time
import SerialPortCommunicator
import math
NB_MOTEUR = 5
CW = 0
CCW = 1
class MoteurRoue:
    def __init__(self):
        self.spc = SerialPortCommunicator.SerialPortCommunicator()


    def stopAllMotors(self):
        self.spc.stopAllMotor()

    def avancerCardinal(self, direction, speed):
        self.beforeChangeDirection()
        if(direction == "N"):
            self.spc.driveMoteur(3, speed, CCW)
            self.spc.driveMoteur(2, speed, CW)
        if(direction == "S"):
            self.spc.driveMoteur(3, speed, CW)
            self.spc.driveMoteur(2, speed, CCW)
        if(direction == "W"):
            self.spc.driveMoteur(1, speed, CCW)
            self.spc.driveMoteur(4, speed, CW)
        if(direction == "E"):
            self.spc.driveMoteur(1, speed, CW)
            self.spc.driveMoteur(4, speed, CCW)
        if(direction == "NE"):
            self.spc.driveMoteur(3, speed, CCW)
            self.spc.driveMoteur(2, speed, CW)
            self.spc.driveMoteur(1, speed, CW)
            self.spc.driveMoteur(4, speed, CCW)
        if(direction == "NW"):
            self.spc.driveMoteur(3, speed, CCW)
            self.spc.driveMoteur(2, speed, CW)
            self.spc.driveMoteur(1, speed, CCW)
            self.spc.driveMoteur(4, speed, CW)
        if(direction == "SE"):
            self.spc.driveMoteur(3, speed, CW)
            self.spc.driveMoteur(2, speed, CCW)
            self.spc.driveMoteur(1, speed, CW)
            self.spc.driveMoteur(4, speed, CCW)
        if(direction == "SW"):
            self.spc.driveMoteur(3, speed, CW)
            self.spc.driveMoteur(2, speed, CCW)
            self.spc.driveMoteur(1, speed, CCW)
            self.spc.driveMoteur(4, speed, CW)

    def rotation(self, direction, speed):
        self.beforeChangeDirection()
        if(direction == "CW"):
            for i in range(1, NB_MOTEUR):
                self.spc.driveMoteur(i, speed, CW)
                # time.sleep(0.01)
        elif(direction == "CCW"):
            for i in range(1, NB_MOTEUR):
                self.spc.driveMoteur(i, speed, CCW)

    def beforeChangeDirection(self):
        self.stopAllMotors()
        time.sleep(0.2)


#Distance en centimetre
    def avanceVector(self, x, y):
        self.beforeChangeDirection()
        maxSpeed = 0.15
        xSpeed = maxSpeed
        ySpeed = maxSpeed
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
        time.sleep(timeToTravel)
        self.stopAllMotors()

    def demo(self):
        self.avancerCardinal("W", 0.2)
        time.sleep(2)

        self.avancerCardinal("E", 0.2)
        time.sleep(4)

        self.avancerCardinal("W",0.2)
        time.sleep(2)

        self.stopAllMotors()

    def demo2(self):
        self.avancerCardinal("SW", 0.15)
        time.sleep(2.5)

        self.avancerCardinal("NE", 0.15)
        time.sleep(5)

        self.avancerCardinal("SW",0.15)
        time.sleep(2.5)

        self.stopAllMotors()

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

    def demo4(self):
        self.rotation("CW", 0.1)
        time.sleep(3.6)
        self.stopAllMotors()
        time.sleep(1)
        self.rotation("CCW", 0.1)
        time.sleep(3.6)


if __name__ == '__main__':
    mr = MoteurRoue()
    mr.stopAllMotors()
    time.sleep(0.1)
    mr.demo3()

    mr.stopAllMotors()

