

class PositionAdjuster:
    #Manque un SerialPortCommunication
    def __init__(self, wheelManager, robotVision, maestro):
        self.maestro = maestro
        self.maestro.setSpeed(2, 50)

        self.wheelManager = wheelManager
        self.localVision = robotVision



    def lowerArm(self):
        self.maestro.setTarget(2, 762 * 4)

    def ascendArm(self):
        self.maestro.setTarget(2, 1764 * 4)

    def goForwardToStopApproaching(self):
        self.wheelManager.moveTo((10, 0))

    def goBackwardToGrabTreasure(self):
        self.wheelManager.moveTo((-3, 0))

    def activateMagnet(self):
        print "ManipulateTresor.activeElectroAiment() : Pas encore implementer"
        pass

    def deactivateMagnet(self):
        print "ManipulateTresor.desactiveElectroAiment() : Pas encore implementer"
        pass

    def getCloserToChargingStation(self):
        self.ascendArm()
        while not self.localVision.getCloserToTreasures():
            pass
        self.goForwardToStopApproaching()
        return True


    def stopCharging(self):
        i = 0
        while i < 1000:
            print "ManipuleTresor.approcheStationDeCharge() : Robot is charging"
            i = i + 1
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

        self.deactivateMagnet()
        return True


    



