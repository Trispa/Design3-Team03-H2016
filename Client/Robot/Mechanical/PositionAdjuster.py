

class PositionAdjuster:
    #Manque un SerialPortCommunication
    def __init__(self, wheelManager, visionRobot, maestro):
        self.maestro = maestro
        self.maestro.setSpeed(2, 15)

        self.wheelManager = wheelManager
        self.visionRobot = visionRobot



    def setPositionToTakeTresor(self):
        self.maestro.setTarget(2, 762 * 4)

    def setPositionToSecuriseTresor(self):
        self.maestro.setTarget(2, 1764 * 4)

    def avancePourTerminerApproche(self):
        self.wheelManager.moveTo((3, 0))

    def reculePourGraberTresor(self):
        self.wheelManager.moveTo((-3, 0))

    def activeElectroAiment(self):
        print "ManipulateTresor.activeElectroAiment() : Pas encore implementer"
        pass

    def desactiveElectroAiment(self):
        print "ManipulateTresor.desactiveElectroAiment() : Pas encore implementer"
        pass

    def approcheStationDeCharge(self):
        self.setPositionToSecuriseTresor()
        while not self.visionRobot.approcheVersTresor():
            pass
        self.avancePourTerminerApproche()
        return True


    def chargementTerminer(self):
        i = 0
        while i < 1000:
            print "ManipuleTresor.approcheStationDeCharge() : Robot is charging"
            i = i + 1
        self.wheelManager.moveTo((-10, -10))
        return True

    def approcheDuTresor(self):
        print "debut approche tresors"
        self.setPositionToTakeTresor()
        while not self.visionRobot.approcheVersTresor():
            pass
        self.avancePourTerminerApproche()

        self.activeElectroAiment()

        self.reculePourGraberTresor()
        self.setPositionToSecuriseTresor()

        self.desactiveElectroAiment()
        return True


    



