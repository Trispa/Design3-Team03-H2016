from Client.BaseStation.WorldVision.allColors import *

class ColorFactory():

    def constructColor(self,bgrColor, colorName):
        if colorName== "Red":
            return RedProximity(bgrColor, colorName)
        elif colorName=="Black":
            return Black(bgrColor, colorName)
        elif colorName == "Purple":
            return Purple(bgrColor, colorName)
        elif colorName == "YellowTreasure":
            return YellowTreasure(bgrColor, colorName)
        elif colorName == "YellowTreasureDetect":
            return YellowTreasureDetect(bgrColor, colorName)
        elif colorName == "Everything":
            return Everything(bgrColor, colorName)
        elif colorName == "RedProximity":
            return RedProximity(bgrColor, colorName)
        else:
            return GenericColor(bgrColor, colorName)