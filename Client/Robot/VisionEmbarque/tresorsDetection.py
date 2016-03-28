import numpy as np
import cv2
import time
from Client.Robot.Mechanical.CameraTower import CameraTower
from Client.BaseStation.WorldVision.colorContainer import ColorContainer

class TreasuresDetector:
    mask = 0
    video = cv2.VideoCapture(1)
    largeurTresorPixel = 0
    treasuresAngle = []
    followedTreasure = None

    def __init__(self):
        self.camera = CameraTower()
        self.camera.step = 0.4
        self.centered = False

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
                if abs(width - height) < 15:
                    cv2.rectangle(self.image,(xElementCoordinate,yElementCoordinate),(xElementCoordinate+width,yElementCoordinate+height),(0,255,0),2)
                    if xElementCoordinate > self.xCoordinateToBeHigher:
                        if self.followedTreasure != None:
                            if abs(xElementCoordinate - self.followedTreasure[0]) < 50:
                                self.followedTreasure = cv2.boundingRect(contour)
                                self.xCoordinateToBeHigher = 320
                        else:
                            self.followedTreasure = cv2.boundingRect(contour)

    def detectAndShowImage(self):
        self.setMask()
        self.findContour()

    def isCenteredWithTreasure(self):
        if abs(self.followedTreasure[0] - (self.image.shape[1]/2)) <= 10:
            self.treasuresAngle.append(self.camera.degreeHori)
            print("Ajout d'un tresor a " + str(self.camera.degreeHori) + " degree")
            self.xCoordinateToBeHigher = self.image.shape[1] / 2 + 10
            self.followedTreasure = None
            return True
        return False

    def buildTresorsAngleList(self):

        self.center = True
        self.xCoordinateToBeHigher = 320
        self.camera.moveCameraByAngle(1, 0)
        self.camera.moveCameraByAngle(0, 110)
        self.followedTreasure = None

        while(self.video.isOpened()):

            self.centered = False
            while self.followedTreasure == None:
                ret, self.image = self.video.read()
                self.detectAndShowImage()
                self.camera.moveCameraRight()
                cv2.imshow("Image", self.image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    pass

            while not self.centered:
                ret, self.image = self.video.read()
                self.detectAndShowImage()
                self.camera.moveCameraRight()
                self.centered = self.isCenteredWithTreasure()
                cv2.imshow("Image", self.image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    pass


            cv2.imshow("Image", self.image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.video.release()
        cv2.destroyAllWindows()



if __name__ == "__main__":
    myTreasuresDetector = TreasuresDetector()
    myTreasuresDetector.buildTresorsAngleList()