class PositionAdjusterFactory():
    def createState(self, target):
        if(target == "charging station"):
            return ChargingStationAdjuster()
        elif(target == "treasure"):
            return TreasureAdjuster()
        elif(target == "target"):
            return TargetIslandAdjuster()

class ChargingStationAdjuster():
    def getToTarget(self):
        #Code pour ajuster la position du robot face a la station de charge
        pass

class TreasureAdjuster():
    def getToTarget(self):
        #Code pour ajuster la position du robot face au tresor
        pass

class TargetIslandAdjuster():
    def getToTarget(self):
        #Code pour ajuster la position du robot face a l'ile cible
        pass