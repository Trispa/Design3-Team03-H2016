from Client.BaseStation.WorldVision.allColors import *

class ColorFactory():

    def constructColor(self,bgrColor, colorName):
        if colorName== "Red":
            return Red(bgrColor, colorName)
        elif colorName=="Black":
            return Black(bgrColor, colorName)
        elif colorName == "Pink":
            return Pink(bgrColor, colorName)
        else:
            return GenericColor(bgrColor, colorName)