from worldImage import WorldImage
import os
import base64
import cv2
import platform
from os import system
from threading import Thread, current_thread

class worldVision:

    def __init__(self):
        if platform.system().lower() == "Linux".lower():
            system("v4l2-ctl --device=1 -c brightness=100 -c gain=56 -c exposure_auto=1")
            system("v4l2-ctl --device=1 -c exposure_absolute=275")
            self.camera = cv2.VideoCapture(1)
        else:
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
        ret = True
        frame = None
        for i in range(7):
            old_frame = frame
            ret, frame = self.camera.read()
            if not ret:
                old_frame = frame
                break
        frame = old_frame
        frame = cv2.resize(frame, (960, 720))
        self.mapImage.updateRobotPosition(frame)
        self.mapImage.buildMap(frame)
        self.mapImage.addLabels(frame)
        worldImage = self.mapImage.drawMapOnImage(frame)
        return frame, self.mapImage.getMap()

    def getCurrentMap(self):
        ret, frame = self.camera.read()
        frame = cv2.resize(frame, (960, 720))
        self.mapImage.updateRobotPosition(frame)
        return  self.mapImage.getMap()

    def setTarget(self, target):
        self.mapImage.setTarget(target)

    def setTreasures(self, relativeAngles):
        self.mapImage.defineTreasures(relativeAngles)

    def findBestTresorPosition(self):
        return self.mapImage.findBestTresor()

