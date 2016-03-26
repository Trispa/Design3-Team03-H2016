import numpy as np
import cv2
from math import sqrt, cos, sin, radians
import time
from Client.BaseStation.WorldVision.allColors import GenericColor
import math

# Print seulement les 2 plus gros carre si plus grand que 100
# Detecter une seul grosse forme par couleur
class VisionRobot:
    image = cv2.imread("image/ry1-2.jpg")
    mask = 0
    video = cv2.VideoCapture(1)


    def __init__(self):

        yellowDown = [10, 100, 100]
        yellowUp = [80, 210, 210]

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


        for c in  cnts:
            if cv2.contourArea(c) < 25 and cv2.contourArea(c) > 2:
                x,y,w,h = cv2.boundingRect(c)
                dots.append((x,y,w,h))
                # if max(w, h) > 100 and max(w, h) < 200:

                cv2.rectangle(self.image,(x,y),(x+w,y+h),(0,255,0),2)
                self.addLabels(c)

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

    def goCamera(self):
        while(self.video.isOpened()):
            ret, self.image = self.video.read()

            self.detecColor()
            self.findContour()


            cv2.imshow("Image", self.image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.video.release()
        cv2.destroyAllWindows()



if __name__ == "__main__":
    vr = VisionRobot()

    vr.goCamera()
    # print("distance")
    # print(vr.DistanceAdjascentte(34))
    # vr.detecColor()
    # vr.findContour()