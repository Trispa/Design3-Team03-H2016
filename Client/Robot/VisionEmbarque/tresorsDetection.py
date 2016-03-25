import numpy as np
import cv2
import time
from Client.Robot.Mechanical.CameraTower import CameraTower
from Client.BaseStation.WorldVision.colorContainer import ColorContainer

class VisionRobot:
    image = cv2.imread("image/ry1-2.jpg")
    mask = 0
    video = cv2.VideoCapture(1)
    balayageHori = 0
    LARGEUR_TRESOR_METRE = 2.5
    FOCAL = 508
    largeurTresorPixel = 0
    treasures = []
    treasure = None

    def __init__(self):

        self.camera = CameraTower()
        self.camera.step = 0.4
        self.tresor = None
        self.centered = False

    def detectColor(self):
        coloredImage = cv2.cvtColor(self.image,cv2.COLOR_BGR2HSV)
        blurMapImage = cv2.GaussianBlur(coloredImage, (5, 5), 0)
        self.mask = cv2.inRange(blurMapImage, ColorContainer.yellow.lower, ColorContainer.yellow.higher)

    def findContour(self):
        kernel = np.ones((9,9),np.uint8)
        closing = cv2.morphologyEx(self.mask.copy(), cv2.MORPH_CLOSE, kernel)
        contours, hierarchy = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)
        for contour in contours:
            if len(contour) > 3 and cv2.contourArea(contour) > 1:
                x,y,w,h = cv2.boundingRect(contour)
                if abs(w - h) < 15:
                    cv2.rectangle(self.image,(x,y),(x+w,y+h),(0,255,0),2)
                    self.centered = False
                    if (x+w) > (self.image.shape[1]/2):
                        if self.treasure != None:
                            if (self.treasure[0] - x) < 10:
                                self.treasure = cv2.boundingRect(contour)
                        else:
                            self.treasure = cv2.boundingRect(contour)

    def detectAndShowImage(self):
        self.detectColor()
        self.findContour()

    def isCenteredWithTreasure(self):
        if abs(self.treasure[0] - (self.image.shape[1]/2)) < 5:
            self.treasures.append(self.camera.degreeHori)
            print("Ajout d'un tresor a " + str(self.camera.degreeHori) + " degree")
            self.treausure = None
            return True
        return False

    def goCamera(self):

        self.center = True
        self.camera.moveCameraByAngle(1, 90)
        self.camera.moveCameraByAngle(0, 110)

        while(self.video.isOpened()):
            self.treasure = None
            while self.treasure == None:
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
    vr = VisionRobot()
    vr.goCamera()