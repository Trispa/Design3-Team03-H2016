import cv2
import numpy as np

class Color:

    def __init__(self, bgrColor, colorName):
        dHue = 30
        lowerSaturation = 100
        higherSaturation = 255
        lowerValue = 38
        higherValue = 202
        self.colorName = colorName
        self.hsvColor = cv2.cvtColor(bgrColor,cv2.COLOR_BGR2HSV)
        if colorName != "Red":
            self.lower = np.array([self.hsvColor.item(0) - dHue,lowerSaturation,lowerValue])
            self.higher = np.array([self.hsvColor.item(0) + dHue,higherSaturation,higherValue])
        else:
            self.lower = np.array([150,lowerSaturation,lowerValue])
            self.higher = np.array([179,higherSaturation,higherValue])

    def isInSameColorRange(self, hsvColor):
        print("Color : " + str(self.colorName))
        print("Lower : " + str(self.lower[0]))
        print("Higher : " + str(self.higher[0]))
        print("HueValue " + str(hsvColor.item(0)))
        if (self.isInHueRange(hsvColor.item(0)) and self.isInSaturationRange(hsvColor.item(1)) and self.isInValueRange(hsvColor.item(2))):
            return True
        return False

    def isInHueRange(self, hue):
        if hue >= self.lower[0] and hue <= self.higher[0]:
            return True
        return False

    def isInSaturationRange(self, saturation):
        if saturation > self.lower[1] and saturation < self.higher[1]:
            return True
        return False

    def isInValueRange(self, value):
        if value > self.lower[2] and value < self.higher[2]:
            return True
        return False
