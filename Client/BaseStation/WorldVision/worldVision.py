from worldImage import WorldImage
import os
import base64
import cv2

class worldVision:

    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        self.camera.set(3, 3264)
        self.camera.set(4, 2448)
        self.mapImage = None
        ret, frame = self.camera.read()
        frame = cv2.resize(frame, (960, 720))
        self.mapImage = WorldImage(frame)
        self.mapImage.buildMap(frame)
        self.mapImage.addLabels(frame)
        self.mapImage.updateRobotPosition(frame)

    def initializeRound(self):
        ret, frame = self.camera.read()
        frame = cv2.resize(frame, (960, 720))
        self.mapImage = WorldImage(frame)
        self.mapImage.buildMap(frame)
        self.mapImage.addLabels(frame)
        self.mapImage.updateRobotPosition(frame)

    def getCurrentImage(self):
        ret, frame = self.camera.read()
        frame = cv2.resize(frame, (960, 720))
        self.mapImage.updateRobotPosition(frame)
        worldImage = self.mapImage.drawMapOnImage(frame)
        return worldImage, self.mapImage.getMap()

    def setTarget(self, target):
        self.mapImage.setTarget(target)

