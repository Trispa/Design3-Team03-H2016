import time
import SerialPortCommunicator
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
        time.sleep(0.1)

    def demo(self):
        self.avancerCardinal("W", 0.18)
        time.sleep(2)

        self.avancerCardinal("E", 0.18)
        time.sleep(4)

        self.avancerCardinal("W",0.18)
        time.sleep(2)

        self.stopAllMotors()

    def demo2(self):
        self.avancerCardinal("SW", 0.18)
        time.sleep(2)

        self.avancerCardinal("NE", 0.18)
        time.sleep(4)

        self.avancerCardinal("SW",0.18)
        time.sleep(2)

        self.stopAllMotors()

if __name__ == '__main__':
    mr = MoteurRoue()
    mr.demo()

    # mr.rotation("CCW", 0.1)
    # time.sleep(2)
    # mr.stopAllMotors()
    # time.sleep(1)
    #
    # mr.rotation("CCW", 0.2)
    # time.sleep(1.05)
    # mr.stopAllMotors()
    # time.sleep(1)
    #
    # mr.rotation("CW", 0.2)
    # time.sleep(1.05)
    # mr.stopAllMotors()
    # time.sleep(1)
    #
    # mr.rotation("CCW", 0.2)
    # time.sleep(1.05)
    # mr.stopAllMotors()
    # time.sleep(1)


    # mr.avancerCardinal("N", 0.2)
    # time.sleep(3)
    #
    # mr.avancerCardinal("SW", 0.2)
    # time.sleep(3)
    mr.stopAllMotors()

