import time
from Client.Robot.Movement.WheelManager import WheelManager
from Client.Robot.Mechanical.SerialPortCommunicator import SerialPortCommunicator
from Client.Robot.LocalVision.RobotVision import RobotVision
from Client.Robot.Mechanical.maestro import Controller
from Client.Robot.Mechanical.CameraTower import CameraTower
import cv2

class PositionAdjuster:
    #Manque un SerialPortCommunication
    def __init__(self, wheelManager, robotVision, maestro, spc):
        self.maestro = maestro
        self.maestro.setSpeed(2, 50)
        self.spc = spc

        self.wheelManager = wheelManager
        self.localVision = robotVision



    def lowerArm(self):
        self.maestro.setTarget(2, 762 * 4)

    def ascendArm(self):
        self.maestro.setTarget(2, 1764 * 4)

    def goForwardToStopApproaching(self):
        self.wheelManager.moveTo((30, 0))

    def goBackwardToGrabTreasure(self):
        self.wheelManager.moveTo((-15, 0))

    def activateMagnet(self):
        self.spc.changeCondensatorMode(0)

    def deactivateMagnet(self):
        self.spc.changeCondensatorMode(1)

    def rechargeMagnet(self):
        self.spc.changeCondensatorMode(2)

    def readCondensatorVoltage(self):
        spc.readConsensatorVoltage()

    def getCloserToChargingStation(self):
        self.ascendArm()
        while not self.localVision.getCloserTo(False):
            pass
        self.wheelManager.moveTo((30, 0))
        self.rechargeMagnet()
        return True

    def getCloserToIsland(self):
        self.wheelManager.moveTo((20, 0))
        self.wheelManager.moveTo((0,20))
        self.activateMagnet()
        self.lowerArm()
        time.sleep(2)
        self.deactivateMagnet()
       


    def stopCharging(self):
        self.deactivateMagnet()
        time.sleep(0.5)
        self.wheelManager.moveTo((-20, 0))
        self.wheelManager.moveTo((0, -30))
        return True

    def getCloserToTreasure(self):
        print "debut approche tresors"
        self.lowerArm()
        time.sleep(0.5)
        while not self.localVision.getCloserTo(True):
            pass
        time.sleep(0.5)
        self.activateMagnet()
        time.sleep(0.5)
        self.goForwardToStopApproaching()
        time.sleep(0.5)
        self.goBackwardToGrabTreasure()
        time.sleep(0.5)
        self.ascendArm()
        time.sleep(2)
        self.deactivateMagnet()
        return True

if __name__ == "__main__":
    # __init__(self, wheelManager, robotVision, maestro, spc):
    # def __init__(self, wheelManager, cameraTower, videoCapture):


    m = Controller()
    spc = SerialPortCommunicator()
    wm = WheelManager(spc)

    rv = RobotVision(wm, CameraTower(m), cv2.VideoCapture(0))
    pa = PositionAdjuster(wm, rv, m, spc)

    while True:
        print "Voltage : ", pa.readCondensatorVoltage()
        time.sleep(5)
    # a = raw_input("Press to mode recharge")
    # pa.rechargeMagnet()
    # a = raw_input("Press to mode stop magnet")
    # pa.deactivateMagnet()
    # a = raw_input("Press to start magnet")
    # pa.activateMagnet()
    # a = raw_input("Press to stop magnet")
    # pa.deactivateMagnet()

    



