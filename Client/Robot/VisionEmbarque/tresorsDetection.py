import numpy as np
import cv2
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
    treasures = [0]
    treasure = None

    def __init__(self):

        self.camera = CameraTower()
        self.camera.step = 0.3
        self.tresor = None
        self.centered = False

    def detectColor(self):
        coloredImage = cv2.cvtColor(self.image,cv2.COLOR_BGR2HSV)
        self.mask = cv2.inRange(coloredImage, ColorContainer.yellow.lower, ColorContainer.yellow.higher)

    def findContour(self):
        kernel = np.ones((5,5),np.uint8)
        closing = cv2.morphologyEx(self.mask.copy(), cv2.MORPH_CLOSE, kernel)
        contours, hierarchy = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)
        for contour in contours:
            if len(contour) > 3 and cv2.contourArea(contour) > 15:
                x,y,w,h = cv2.boundingRect(contour)
                if abs(w - h) < 15:
                    cv2.rectangle(self.image,(x,y),(x+w,y+h),(0,255,0),2)
                    self.centered = False
                    if self.treasure != None:
                        if self.treasure < x:
                            self.treasure = cv2.boundingRect(contour)
                    else:
                        self.treasure = cv2.boundingRect(contour)
                    return

    def detectAndShowImage(self):
        self.detectColor()
        self.findContour()

    def isCenteredWithTreasure(self):
        pass

    def goCamera(self):

        self.center = True
        self.camera.moveCameraByAngle(1, 150)
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