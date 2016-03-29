

class GrabTresor:
    def __init__(self, spc, maestro):
        self.maestro = maestro
        self.spc = spc

        self.maestro.setSpeed(2, 15)


    def setPositionToTakeTresor(self):
        self.maestro.setTarget(2, 762.5 * 4)

    def setPositionToSecuriseTresor(self):
        self.maestro.setTarget(2, 1764.25 * 4)

