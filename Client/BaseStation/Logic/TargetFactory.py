from TargetTypes import *

class TargetFactory():
    def constructTarget(self, target):
        if("forme" in target):
            return ShapeTarget(target["forme"])
        elif("couleur" in target):
            return ColorTarget(target["couleur"])
