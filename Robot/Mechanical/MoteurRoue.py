import time
import SerialPortCommunicator
NB_MOTEUR = 5
CW = 0
CCW = 1
class MoteurRoue:
    def __init__(self):
        self.spc = SerialPortCommunicator.SerialPortCommunicator()


    def stopAllMotors(self):
        for i in range(1, NB_MOTEUR):
            self.spc.driveMoteur(i, 0, 0)

    def avancerCardinal(self, direction, speed):
        if(direction.find("N") != -1):
            self.spc.driveMoteur(1, speed*100, CCW)
            self.spc.driveMoteur(4, speed*100, CW)
        if(direction.find("S") != -1):
            self.spc.driveMoteur(1, speed*100, CW)
            self.spc.driveMoteur(4, speed*100, CCW)
        if(direction.find("W") != -1):
            self.spc.driveMoteur(3, speed*100, CCW)
            self.spc.driveMoteur(2, speed*100, CW)
        if(direction.find("E") != -1):
            self.spc.driveMoteur(3, speed*100, CW)
            self.spc.driveMoteur(2, speed*100, CCW)

    def rotation(self, direction, speed):
        if(direction == "CW"):
            for i in range(1, NB_MOTEUR):
                self.spc.driveMoteur(i, speed * 100, CW)
        elif(direction == "CCW"):
            for i in range(1, NB_MOTEUR):
                self.spc.driveMoteur(i, speed * 100, CCW)

if __name__ == '__main__':
    mr = MoteurRoue()
    mr.rotation("CW", 0.2)
    time.sleep(4)
    mr.stopAllMotors()

