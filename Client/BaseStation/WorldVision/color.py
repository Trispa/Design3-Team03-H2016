import cv2
import numpy as np

class Color:

    def __init__(self, bgrColor, colorName):
        dHue = 30
        lowerSV = 60
        higherSV = 255
        self.colorName = colorName
        self.hsvColor = cv2.cvtColor(bgrColor,cv2.COLOR_BGR2HSV)
        self.lower = np.array([self.hsvColor.item(0) - dHue,lowerSV,lowerSV])
        self.higher = np.array([self.hsvColor.item(0) + dHue,higherSV,higherSV])