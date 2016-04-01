import numpy as np
import cv2
from Client.Robot.Mechanical.CameraTower import CameraTower
from Client.BaseStation.WorldVision.colorContainer import ColorContainer

class TreasuresDetector:
    MAX_LENGHT_DIFFERENCE = 15
    MAX_PIXEL_FROM_FOLLOWED_TREASURE = 50
    START_CAMERA_HORIZONTAL_ANGLE = 0
    START_CAMERA_VERTICAL_ANGLE = 50
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
        blurMapImage = cv2.GaussianBlur(self.image, (5, 5), 0)
        coloredImage = cv2.cvtColor(blurMapImage,cv2.COLOR_BGR2HSV)
        self.mask = cv2.inRange(coloredImage, ColorContainer.yellow.lower, ColorContainer.yellow.higher)

    def findContour(self):
        kernel = np.ones((5,5),np.uint8)
        closing = cv2.morphologyEx(self.mask.copy(), cv2.MORPH_CLOSE, kernel)
        contours, hierarchy = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)
        for contour in contours:
            if len(contour) > 3 and cv2.contourArea(contour) > 1 and cv2.contourArea(contour) < 500:
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
            alreadyAdded = False
            for angle in self.treasuresAngle:
                if self.camera.degreeHori - angle < 2:
                    averageAngle = (angle + self.camera.degreeHori) / 2
                    self.treasuresAngle.remove(angle)
                    self.treasuresAngle.append(averageAngle)
                    alreadyAdded = True
                    break
            if not alreadyAdded:
                self.treasuresAngle.append(self.camera.degreeHori)
            self.xCoordinateToBeHigher = self.image.shape[1] / 2 + self.ACCEPTABLE_PIXEL_DIFFERENCE + 10
            self.followedTreasure = None
            return True
        return False

    def buildTresorsAngleList(self):

        self.center = True
        self.camera.moveCameraByAngle(1, self.START_CAMERA_HORIZONTAL_ANGLE)
        self.camera.moveCameraByAngle(0, self.START_CAMERA_VERTICAL_ANGLE)
        self.followedTreasure = None

        while(self.video.isOpened() and self.camera.degreeHori < 173):

            self.centered = False
            ret, self.image = self.video.read()
            self.xCoordinateToBeHigher = self.image.shape[1] / 2
            while self.followedTreasure == None and self.camera.degreeHori < 173:
                ret, self.image = self.video.read()
                self.detectAndShowImage()
                self.camera.moveCameraRight()

            while not self.centered and self.camera.degreeHori < 173:
                ret, self.image = self.video.read()
                self.detectAndShowImage()
                self.camera.moveCameraRight()
                self.centered = self.isCenteredWithTreasure()

        self.video.release()
        print("Liste des angles : ", self.treasuresAngle)
        return self.treasuresAngle



if __name__ == "__main__":
    myTreasuresDetector = TreasuresDetector(CameraTower(), cv2.VideoCapture(0))
    myTreasuresDetector.buildTresorsAngleList()
