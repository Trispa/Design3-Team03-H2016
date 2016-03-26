import numpy as np
import cv2
from math import sqrt, cos, sin, radians
import time
from Client.Robot.Mechanical.CameraTower import CameraTower
import math
from matplotlib import pyplot as plt
import argparse
import glob
import cv2


class VisionEdgeDetection:

    img = cv2.imread("image/image1.jpg")
    mask = 0
    # video = cv2.VideoCapture(1)

    def __init__(self, img):
        self.img = cv2.imread(img)


    def goCamera(self):

        # while(self.video.isOpened()):
            # ret, self.image = self.video.read()

        ret,thresh1 = cv2.threshold(self.img,100,255,cv2.THRESH_BINARY)


        ih, iw, ic = self.img.shape
        col1 = 0
        col2 = iw - 1
        dot1 = []
        dot2 = []

        while dot1 == [] or dot2 == []:
            if dot1 == []:
                col1 = col1 + 1
                for i in range(0, ih):
                    if np.equal(thresh1[i, 0], np.array([255,255,255])).all():
                        dot1 = (0, i)
                        break

            if dot2 == []:
                col2 = col2 - 1
                for i in range(0, ih):
                    if np.equal(thresh1[i, col2], np.array([255, 255, 255])).all():
                        dot2 = (col2, i)
                        break

        print dot1
        print dot2
        # dot1 = (1279, 0)

        cv2.line(thresh1, dot1, dot2, (255, 0, 0), 2)
        cv2.line(thresh1, (dot1[0], (dot1[1] + dot2[1])/2), (dot2[0], (dot1[1] + dot2[1])/2),(0, 0, 255), 2)
        print dot1[1] - (dot1[1] + dot2[1])/2
        cv2.imshow("Image", thresh1)
        cv2.waitKey(0)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
            # self.video.release()
        cv2.destroyAllWindows()




if __name__ == "__main__":
    ved = VisionEdgeDetection()
    ved.goCamera()
