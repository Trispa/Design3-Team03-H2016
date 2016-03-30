import numpy as np
import cv2
import time
from Client.BaseStation.WorldVision.colorContainer import ColorContainer

class TreasuresDetector:
    MAX_LENGHT_DIFFERENCE = 15
    MAX_PIXEL_FROM_FOLLOWED_TREASURE = 50
    START_CAMERA_HORIZONTAL_ANGLE = 0
    START_CAMERA_VERTICAL_ANGLE = 110
    ACCEPTABLE_PIXEL_DIFFERENCE = 10
    mask = 0
    treasuresAngle = []
    followedTreasure = None

    def __init__(self, cameraTower, video):
        self.camera = cameraTower
        self.camera.step = 0.4
        self.centered = False
        self.video = video

    def setMask(self):
        coloredImage = cv2.cvtColor(self.image,cv2.COLOR_BGR2HSV)
        blurMapImage = cv2.GaussianBlur(coloredImage, (5, 5), 0)
        self.mask = cv2.inRange(blurMapImage, ColorContainer.yellow.lower, ColorContainer.yellow.higher)

    def findContour(self):
        kernel = np.ones((5,5),np.uint8)
        closing = cv2.morphologyEx(self.mask.copy(), cv2.MORPH_CLOSE, kernel)
        contours, hierarchy = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)
        for contour in contours:
            if len(contour) > 3 and cv2.contourArea(contour) > 1:
                xElementCoordinate,yElementCoordinate,width,height = cv2.boundingRect(contour)
                if abs(width - height) < self.MAX_LENGHT_DIFFERENCE:
                    cv2.rectangle(self.image,(xElementCoordinate,yElementCoordinate),(xElementCoordinate+width,yElementCoordinate+height),(0,255,0),2)
                    if xElementCoordinate > self.xCoordinateToBeHigher:
                        if self.followedTreasure != None:
                            if abs(xElementCoordinate - self.followedTreasure[0]) < self.MAX_PIXEL_FROM_FOLLOWED_TREASURE:
                                self.followedTreasure = cv2.boundingRect(contour)
                                self.xCoordinateToBeHigher = self.image.shape[1] / 2
                        else:
                            self.followedTreasure = cv2.boundingRect(contour)

    def detectAndShowImage(self):
        self.setMask()
        self.findContour()

    def isCenteredWithTreasure(self):
        if abs(self.followedTreasure[0] - (self.image.shape[1]/2)) <= self.ACCEPTABLE_PIXEL_DIFFERENCE:
            self.treasuresAngle.append(self.camera.degreeHori)
            print("Ajout d'un tresor a " + str(self.camera.degreeHori) + " degree")
            self.xCoordinateToBeHigher = self.image.shape[1] / 2 + self.ACCEPTABLE_PIXEL_DIFFERENCE
            self.followedTreasure = None
            return True
        return False

    def buildTresorsAngleList(self):

        self.center = True
        self.camera.moveCameraByAngle(1, self.START_CAMERA_HORIZONTAL_ANGLE)
        self.camera.moveCameraByAngle(0, self.START_CAMERA_VERTICAL_ANGLE)
        self.followedTreasure = None

        while(self.video.isOpened() and self.camera.degreeHori != 180):

            self.centered = False
            ret, self.image = self.video.read()
            self.xCoordinateToBeHigher = self.image.shape[1] / 2
            while self.followedTreasure == None:
                ret, self.image = self.video.read()
                self.detectAndShowImage()
                self.camera.moveCameraRight()

            while not self.centered:
                ret, self.image = self.video.read()
                self.detectAndShowImage()
                self.camera.moveCameraRight()
                self.centered = self.isCenteredWithTreasure()

        self.video.release()
        return self.treasuresAngle



if __name__ == "__main__":
    myTreasuresDetector = TreasuresDetector()
    myTreasuresDetector.buildTresorsAngleList()