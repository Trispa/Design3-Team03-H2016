from worldImage import WorldImage
import os
import base64
import cv2

class worldVision:

    def __init__(self):
        self.camera = cv2.VideoCapture(2)


    def getCurrentImage(self):

        ret, frame = self.camera.read()
        geometricalImage = WorldImage(frame)
        geometricalImage.setMap()
        geometricalImage.addLabels()

        worldImage = geometricalImage.drawMapOnImage()

        return worldImage


