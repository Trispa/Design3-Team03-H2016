import cv2
import numpy as np

class Color:

    def __init__(self, bgrColor, colorName):
        self.dHue = 30
        self.colorName = colorName
        self.hsvColor = cv2.cvtColor(bgrColor,cv2.COLOR_BGR2HSV)

    def isInSameColorRange(self, hsvColor):
        if (self.isInHueRange(hsvColor.item(0)) and self.isInSaturationRange(hsvColor.item(1)) and self.isInValueRange(hsvColor.item(2))):
            return True
        return False

    def isInHueRange(self, hue):
        if hue >= self.lower[0] and hue <= self.higher[0]:
            return True
        return False

    def isInSaturationRange(self, saturation):
        if saturation >= self.lower[1] and saturation <= self.higher[1]:
            return True
        return False

    def isInValueRange(self, value):
        if value > self.lower[2] and value < self.higher[2]:
            return True
        return False

    def getName(self):
        return self.colorName


class GenericColor(Color):
    def __init__(self, bgrColor, colorName):
        Color.__init__(self, bgrColor, colorName)

        lowerSaturation = 100
        higherSaturation = 255
        lowerValue = 38
        higherValue = 255

        self.lower = np.array([self.hsvColor.item(0) - self.dHue,lowerSaturation,lowerValue])
        self.higher = np.array([self.hsvColor.item(0) + self.dHue,higherSaturation,higherValue])


class Black(Color):
    def __init__(self, bgrColor, colorName):
        Color.__init__(self, bgrColor, colorName)
        lowerValue = 0
        higherValue = 80
        lowerSaturation = 0
        higherSaturation = 255
        self.lower = np.array([0,lowerSaturation,lowerValue])
        self.higher = np.array([179,higherSaturation,higherValue])

class Pink(Color):
    def __init__(self, bgrColor, colorName):
        Color.__init__(self, bgrColor, colorName)
        lowerValue = 127
        higherValue = 255
        lowerSaturation = 33
        higherSaturation = 255
        self.lower = np.array([115,lowerSaturation,lowerValue])
        self.higher = np.array([179,higherSaturation,higherValue])

class Red(Color):
    def __init__(self, bgrColor, colorName):
        Color.__init__(self, bgrColor, colorName)

        lowerSaturation = 100
        higherSaturation = 255
        lowerValue = 38
        higherValue = 202

        self.lower = np.array([150,lowerSaturation,lowerValue])
        self.higher = np.array([179,higherSaturation,higherValue])

    def isInHueRange(self, hue):
        if (hue >= self.lower[0] and hue <= self.higher[0]) or hue >= 0 and hue <= 8:
            return True
        return False


