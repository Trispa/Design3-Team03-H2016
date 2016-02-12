import worldImage
import cv2
import numpy as np

class WorldVision:

    def __init__(self, frame):
        self.__worldImage = worldImage.WorldImage(frame)

    def printOriginalWorld(self):
        cv2.imshow("Orginal world", self.__worldImage.drawMapOnImage())
        cv2.waitKey(0)

    def printDrawnWorld(self):
        self.__worldImage.setMap("AllFilter")
        self.__worldImage.addLabels()
        myWorld = self.__worldImage.drawMapOnImage()
        cv2.imshow("Drawn world", myWorld)
        cv2.waitKey(0)

