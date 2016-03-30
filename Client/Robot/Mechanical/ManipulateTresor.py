

class GrabTresor:
    #Manque un SerialPortCommunication
    def __init__(self, wheelManager, visionRobot, maestro):
        self.maestro = maestro
        self.maestro.setSpeed(2, 15)

        self.wheelManager = wheelManager
        self.visionRobot = visionRobot



    def setPositionToTakeTresor(self):
        self.maestro.setTarget(2, 762.5 * 4)

    def setPositionToSecuriseTresor(self):
        self.maestro.setTarget(2, 1764.25 * 4)

    def approcheDuTresor(self):
        while not self.visionRobot.approcheVersTresor():
            pass
        return True

    def derniereApprochePourGraberLeTresor(self):
        self.wheelManager.moveTo((3, 0))

    def reculePourMonterElectroAimant(self):
        self.wheelManager.moveTo((-3, 0))

    def activeElectroAiment(self):
        print "ManipulateTresor.activeElectroAiment() : Pas encore implementer"
        pass

    def desactiveElectroAiment(self):
        print "ManipulateTresor.desactiveElectroAiment() : Pas encore implementer"
        pass
    



