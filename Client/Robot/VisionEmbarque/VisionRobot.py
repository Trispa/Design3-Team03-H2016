import math
from math import sqrt, cos, sin, radians
from os import system

import cv2
import numpy as np

from Client.Robot.Logic.Deplacement.WheelManager import WheelManager
from Client.Robot.Mechanical.CameraTower import CameraTower
import platform


class VisionRobot:
    mask = 0
    if platform.linux_distribution()[0].lower() == "Ubuntu".lower():
        video = cv2.VideoCapture(1)
        system("v4l2-ctl --device=1 --set-ctrl gain=50")
    elif platform.linux_distribution()[0].lower() == "Fedora".lower():
        video = cv2.VideoCapture(0)
        system("v4l2-ctl --device=0 --set-ctrl gain=0 -c brightness=80")

    balayageHori = 0
    LARGEUR_TRESOR_METRE = 2.5
    FOCAL = 508
    largeurTresorPixel = 0

    def __init__(self, moteurRoue, cameraTower):

        self.robot = moteurRoue
        self.camera = cameraTower
        self.camera.step = 0.5
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

            if cv2.contourArea(cntsMax) > 100:
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
            square = 18

            xob = (iw/2-5)  - square/2
            yob = ih/2 - square/2
            # print xob, yob
            # print xob + square, yob +square

            cv2.rectangle(self.image,(xob, yob),(xob + square-3, yob + square+7),(0,0,255),2)
            # cv2.rectangle(self.image,(x,y),(x+w,y+h),(0,255,0),2)

            if x <= (iw/2 - square-3):
                self.camera.moveCameraLeft()
            elif x >= (iw/2 + square-3):
                self.camera.moveCameraRight()
            else:
                centerX = True
            if y <= (ih/2 - square+7):
                self.camera.moveCameraUp()
            elif y >= (ih/2 + square+7):
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

    def diffLigneParralelle(self):
        ret,thresh1 = cv2.threshold(self.image,125,255,cv2.THRESH_BINARY)


        ih, iw, ic = self.image.shape
        col1 = 0
        col2 = iw - 1
        dot1 = []
        dot2 = []


        col1 = col1 + 1
        for i in range(0, ih):
            if np.equal(thresh1[i, 0], np.array([255,255,255])).all():
                dot1 = (0, i)
                break
            if dot1 == []:
                dot1 = (0, ih-1)

        for i in range(0, ih):
            if np.equal(thresh1[i, col2], np.array([255, 255, 255])).all():
                dot2 = (col2, i)
                break
            if dot2 == []:
                for i in range(iw - 1, -1, -1):
                    if np.equal(thresh1[ih - 1, i], np.array([255, 255, 255])).all():
                        dot2 = (col2, i)
                        break

        # print dot1
        # print dot2
        # dot1 = (1279, 0)
        self.image = thresh1

        cv2.line(self.image, dot1, dot2, (255, 0, 0), 2)
        cv2.line(self.image, (dot1[0], (dot1[1] + dot2[1])/2), (dot2[0], (dot1[1] + dot2[1])/2),(0, 0, 255), 2)
        distancePixel = dot1[1] - (dot1[1] + dot2[1])/2
        # print distancePixel
        return distancePixel


    def approcheVersTresor(self):
        findSomething = False
        center = False
        movingY = False
        moveYArriver = False
        movingX = False
        moveXArriver = False
        lastAngle= 0


        self.camera.moveCameraByAngle(1, 50)
        self.camera.moveCameraByAngle(0, 30)

        while(self.video.isOpened()):
            ret, self.image = self.video.read()
            self.detecColor()
            self.findContour()

            if not findSomething:
                # print "findSomething"
                findSomething = self.balayageCamera()

            if self.tresor == None:
                findSomething = False
                movingY = False
                moveYArriver = False
                movingX = False
                moveXArriver = False



            center = self.moveCameraEmbarquee()

            if center and not self.robot.isMoving:
                if not movingY and not moveYArriver:
                    diff = self.diffLigneParralelle()
                    if diff < 0:
                        self.robot.moveToInfinit(0,-30)
                    else:
                        self.robot.moveToInfinit(0,30)
                    movingY = True

                if moveYArriver:
                    if not movingX and not moveXArriver:
                        self.robot.moveToInfinit(30, 0)
                        movingX = True

            if movingY and not moveYArriver:
                if abs(self.diffLigneParralelle()) < 8:
                    self.robot.stopAllMotors()
                    moveYArriver = True
                    movingY = False


            if movingX and not moveXArriver:
                print self.camera.degreeVerti


                if self.camera.degreeVerti <= 7:
                    self.robot.stopAllMotors()
                    moveXArriver = True
                elif self.camera.degreeVerti <= lastAngle - 0.5:
                    self.robot.stopAllMotors()
                    # moveXArriver = True
                    moveYArriver = False
                    movingX = False
                    lastAngle = self.camera.degreeVerti



            if moveYArriver and moveXArriver:
                print "!!! ARRIVER !!!"
                return True

            # cv2.imshow("Image", self.image)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
        # self.video.release()
        # cv2.destroyAllWindows()


if __name__ == "__main__":
    mr = WheelManager()
    ct = CameraTower()
    vr = VisionRobot(mr, ct)

    vr.approcheVersTresor()
    # vr.goDetectTresorAround()
    # print("distance")
    # print(vr.DistanceAdjascentte(34))
    # vr.detecColor()
    # vr.findContour()