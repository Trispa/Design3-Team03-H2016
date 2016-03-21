import numpy as np
import cv2
from math import sqrt, cos, sin, radians
import time
from Client.BaseStation.WorldVision.allColors import GenericColor
from Client.Robot.Mechanical.CameraTower import CameraTower
import math
from Client.Robot.Mechanical.MoteurRoue import MoteurRoue

# Print seulement les 2 plus gros carre si plus grand que 100
# Detecter une seul grosse forme par couleur
class VisionRobot:
    image = cv2.imread("image/ry1-2.jpg")
    mask = 0
    video = cv2.VideoCapture(1)
    balayageHori = 0
    LARGEUR_TRESOR_METRE = 2.5
    FOCAL = 508
    largeurTresorPixel = 0

    def __init__(self):

        self.robot = MoteurRoue()
        self.camera = CameraTower()
        self.camera.step = 1
        self.tresor = None
        yellowDown = [0, 100, 100]
        yellowUp = [35, 255, 255]

        # yellow = colorFactory.constructColor(np.uint8([[[0,255,255]]]), "Yellow")
        redDown = [0, 0, 80]
        redUp = [85, 40, 255]

        # self.color = [(yellow.lower, yellow.higher), (redDown, redUp)]
        self.color = [(yellowDown, yellowUp)]

    def detecColor(self):
        self.mask = 0
        for(lower, upper) in self.color:
            lower = np.array(lower, dtype = "uint8")
            upper = np.array(upper, dtype="uint8")

            self.mask = self.mask + cv2.inRange(self.image, lower, upper)

    def findContour(self):

        (cnts, _) = cv2.findContours(self.mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)
        dots = []
        if len(cnts):

            cntsMax = cnts[0]
            for c in cnts:
                if cv2.contourArea(c) > cv2.contourArea(cntsMax):
                    cntsMax = c

            if cv2.contourArea(cntsMax) > 200:
                self.tresor = cntsMax
                x,y,w,h = cv2.boundingRect(self.tresor)
                dots.append((x,y,w,h))
                # if max(w, h) > 100 and max(w, h) < 200:

                cv2.rectangle(self.image,(x,y),(x+w,y+h),(0,255,0),2)
                self.addLabels(self.tresor)

                self.largeurTresorPixel = max(w,h)
                return self.largeurTresorPixel
            else:
                self.tresor = None
            return 0



    def addLabelsLines(self, dots):
        if len(dots) > 1:
            dotx1 = int(dots[0][2]/2) + dots[0][0]
            dotx2 = int(dots[1][2]/2) + dots[1][0]
            doty1 = int(dots[0][3]/2) + dots[0][1]
            doty2 = int(dots[1][3]/2) + dots[1][1]
            dot1 = (dotx1, doty1)
            dot2 = (dotx2, doty2)

            dots = (dot1, dot2)

            cv2.line(self.image, dots[0], dots[1], (255, 0, 0), 2)
            distance = int(sqrt((dots[0][0] - dots[1][0])**2 + (dots[0][1] - dots[1][1])**2))
            xlabel = int(abs(dots[0][0] - dots[1][0])/2) + min(dots[0][0], dots[1][0])
            ylabel = int(abs(dots[0][1] - dots[1][1])/2) + min(dots[0][1], dots[1][1])
            labelDot = (xlabel, ylabel)

            cv2.putText(self.image, str(distance), labelDot, cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,255), 1, 8)
            return distance

    def addLabels(self, c):
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.4
        thickness = 1

        size, baseline = cv2.getTextSize("pixel", font, scale, thickness)
        textWidth = size[0]
        textHeight = size[1]
        x,y,w,h = cv2.boundingRect(c)
        point = (x, y - 5)
        cv2.putText(self.image, "Position " + str(x) + " " + str(y) + " " + str(max(w, h)) + " pixel, " + str(cv2.contourArea(c)) + " area", point, font, scale, (0,0,255), thickness, 8)


    def moveCameraEmbarquee(self):
        centerX = False
        centerY = False
        if self.tresor != None:

            x,y,w,h = cv2.boundingRect(self.tresor)
            ih, iw, ic = self.image.shape
            # print x, y, iw, ih
            square = 20

            xob = iw/2  - square
            yob = ih/2 - square
            # print xob, yob

            cv2.rectangle(self.image,(xob, yob),(xob + 2*square, yob - 2*square),(0,255,0),2)

            if x <= (iw/2 - square):
                self.camera.moveCameraLeft()
            elif x >= (iw/2 + square):
                self.camera.moveCameraRight()
            else:
                centerX = True
            if y <= (ih/2 - square):
                self.camera.moveCameraUp()
            elif y >= (ih/2 + square):
                self.camera.moveCameraDown()
            else:
                centerY = True

        return centerX and centerY

    def balayageCamera(self):
        if self.tresor == None:
            if self.balayageHori == 0 and self.camera.degreeHori < 160:
                self.camera.moveCameraRight()
            else:
                self.balayageHori = 1
                self.camera.moveCameraByAngle(0, 90)

            if self.balayageHori == 1 and self.camera.degreeHori > 55:
                self.camera.moveCameraLeft()
            else:
                self.balayageHori = 0

        else:
            return True
        return False


    def distanceAdjascente(self):
            if self.largeurTresorPixel <= 0:
                return 0
            return self.FOCAL * self.LARGEUR_TRESOR_METRE / self.largeurTresorPixel

    def distanceFromCamera(self):
        distanceY = self.distanceAdjascente() * cos(radians(123 - self.camera.degreeHori) + math.pi/2)
        distanceX = self.distanceAdjascente() * sin(radians(self.camera.degreeVerti - 64))
        # print 123 - self.camera.degreeHori, self.camera.degreeVerti, self.distanceAdjascente()

        return (distanceX, distanceY)

    def goCamera(self):
        findSomething = False
        center = False
        self.camera.moveCameraByAngle(1, 0)
        self.camera.moveCameraByAngle(0, 80)
        while(self.video.isOpened()):
            ret, self.image = self.video.read()
            if not findSomething:
                findSomething = self.balayageCamera()
            self.detecColor()
            self.findContour()
            center = self.moveCameraEmbarquee()
            dis = self.distanceFromCamera()
            print dis

            if not self.robot.isRunning and center:
                self.approcheDuRobot(self.distanceFromCamera())

            cv2.imshow("Image", self.image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.video.release()
        cv2.destroyAllWindows()

    def approcheDuRobot(self, distanceDuTresor):
        if abs(distanceDuTresor[0]) > 1:
            self.robot.avanceVector(distanceDuTresor[0], 0)

        elif abs(distanceDuTresor[1]) > 1:
            self.robot.avanceVector(0, distanceDuTresor[1])


if __name__ == "__main__":
    vr = VisionRobot()

    vr.goCamera()
    # print("distance")
    # print(vr.DistanceAdjascentte(34))
    # vr.detecColor()
    # vr.findContour()