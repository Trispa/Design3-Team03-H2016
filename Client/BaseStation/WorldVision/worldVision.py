from worldImage import WorldImage
import os
import base64
import cv2

class worldVision:

    def __init__(self):
        self.camera = cv2.VideoCapture(1)
        self.camera.set(3, 720)
        self.camera.set(4, 720)
        ret, frame = self.camera.read()
        self.mapImage = WorldImage(frame)

    def getCurrentImage(self):

        ret, frame = self.camera.read()
        self.mapImage.setMap(frame)
        self.mapImage.addLabels(frame)
        worldImage = self.mapImage.drawMapOnImage(frame)

        return worldImage


