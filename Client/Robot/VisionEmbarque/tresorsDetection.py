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
        self.camera.step = 0.5
        self.tresor = None
        self.centered = False

    def detectColor(self):
        coloredImage = cv2.cvtColor(self.image,cv2.COLOR_BGR2HSV)
        blurMapImage = cv2.GaussianBlur(coloredImage, (5, 5), 0)
        self.mask = cv2.inRange(blurMapImage, ColorContainer.yellow.lower, ColorContainer.yellow.higher)

    def findContour(self):
        kernel = np.ones((5,5),np.uint8)
        closing = cv2.morphologyEx(self.mask.copy(), cv2.MORPH_CLOSE, kernel)
        contours, hierarchy = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)
        for contour in contours:
            if len(contour) > 3 and cv2.contourArea(contour) > 1:
                x,y,w,h = cv2.boundingRect(contour)
                if abs(w - h) < 15:
                    cv2.rectangle(self.image,(x,y),(x+w,y+h),(0,255,0),2)
                    if x > self.xMin:
                        if self.treasure != None:
                            if abs(x - self.treasure[0]) < 50:
                                self.treasure = cv2.boundingRect(contour)
                                self.xMin = 320
                        else:
                            self.treasure = cv2.boundingRect(contour)

    def detectAndShowImage(self):
        self.detectColor()
        self.findContour()

    def isCenteredWithTreasure(self):
        if abs(self.treasure[0] - (self.image.shape[1]/2)) <= 10:
            self.treasures.append(self.camera.degreeHori)
            print("Ajout d'un tresor a " + str(self.camera.degreeHori) + " degree")
            self.xMin = self.image.shape[1] / 2 + 10
            self.treasure = None
            return True
        return False

    def goCamera(self):

        self.center = True
        self.xMin = 320
        self.camera.moveCameraByAngle(1, 80)
        self.camera.moveCameraByAngle(0, 110)
        self.treasure = None

        while(self.video.isOpened()):

            self.centered = False
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