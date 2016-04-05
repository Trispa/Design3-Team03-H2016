import time
from Client.Robot.Movement.WheelManager import WheelManager
from Client.Robot.Mechanical.SerialPortCommunicator import SerialPortCommunicator
from Client.Robot.LocalVision.RobotVision import RobotVision
from Client.Robot.Mechanical.maestro import Controller

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
        self.wheelManager.moveTo((-3, 0))

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
        while not self.localVision.getCloserToChargingStation():
            pass
        self.goForwardToStopApproaching()
        self.rechargeMagnet()
        return True


    def stopCharging(self):
        i = 0
        while i < 1000:
            print "ManipuleTresor.approcheStationDeCharge() : Robot is charging"
            i = i + 1
        self.deactivateMagnet()
        self.wheelManager.moveTo((-10, -10))
        return True

    def getCloserToTreasure(self):
        print "debut approche tresors"
        self.lowerArm()
        while not self.localVision.getCloserToTreasures():
            pass
        self.goForwardToStopApproaching()

        self.activateMagnet()

        self.goBackwardToGrabTreasure()
        self.ascendArm()
        time.sleep(1)
        self.deactivateMagnet()
        return True

if __name__ == "__main__":
    # __init__(self, wheelManager, robotVision, maestro, spc):
    wm = WheelManager()
    rv = RobotVision()
    m = Controller()
    spc = SerialPortCommunicator()

    pa = PositionAdjuster(wm, rv, m, spc)

    while True:
        print pa.readCondensatorVoltage()

    



