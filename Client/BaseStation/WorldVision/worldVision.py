from worldImage import WorldImage
import os
import base64
import cv2

class worldVision:

    def __init__(self):
        self.camera = cv2.VideoCapture(1)
        self.camera.set(3, 720)
        self.camera.set(4, 960)
        ret, frame = self.camera.read()
        #frame = cv2.imread('WorldVisionTest/Photo-Test/Frames/Picture 212.jpg')

        self.mapImage = WorldImage(frame)

    def getCurrentImage(self):

        ret, frame = self.camera.read()
        #frame = cv2.imread('WorldVisionTest/Photo-Test/Frames/Picture 212.jpg')

        self.mapImage.buildMap(frame)
        self.mapImage.addLabels(frame)
        worldImage = self.mapImage.drawMapOnImage(frame)

        return worldImage

    def getCurrentMap(self):
        return self.mapImage.getMap()


