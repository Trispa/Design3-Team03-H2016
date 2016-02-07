import cv2
import numpy as np
import random
import time
import math
import Movement

class RobotMock:
    def __init__(self):
        self.isMoving = False
        self.orientation = 0;
        self.positionX = random.randrange(100, 900)
        self.positionY = random.randrange(100, 500)

        self.__displayMock()


    def move(self, pointToMoveTo):
        self.isMoving = True
        #dans la classe qui serais Movement
        deplacementX = pointToMoveTo.__getitem__(0) - self.positionX
        deplacementY = pointToMoveTo.__getitem__(1) - self.positionY
        deplacementTotal = float(abs(deplacementX) +abs(deplacementY))

        #set la vitesse des "roues"
        vitesseX = int(math.ceil(20*(deplacementX/deplacementTotal)))
        vitesseY = int(math.ceil(20*(deplacementY/deplacementTotal)))

        while deplacementX != 0 or deplacementY != 0:
            deplacementX = self.__deplacementX(deplacementX, vitesseX)
            deplacementY = self.__deplacementY(deplacementY, vitesseY)
            self.__displayMouvement()

        self.isMoving = False


    def __deplacementY(self, deplacementY, vitesseY):
        if abs(deplacementY) >= abs(vitesseY) and deplacementY != 0 and vitesseY != 0:
            self.positionY += vitesseY
            deplacementY -= vitesseY
        else:
            self.positionY += deplacementY
            deplacementY = 0
        return deplacementY


    def __deplacementX(self, deplacementX, vitesseX):
        if abs(deplacementX) >= abs(vitesseX) and deplacementX != 0 and vitesseX != 0:
            self.positionX += vitesseX
            deplacementX -= vitesseX
        else:
            self.positionX += deplacementX
            deplacementX = 0
        return deplacementX


    def __displayMouvement(self):
        img = np.zeros((512, 1000, 3), np.uint8, 'C')
        cv2.rectangle(img, (self.positionX - 20, self.positionY - 20), (self.positionX + 20, self.positionY + 20),
                      (0, 255, 0), -1, 1)
        cv2.imshow('image', img)
        cv2.waitKey(1)
        time.sleep(0.05)


    def __displayMock(self):
            #mouse callback function
            def mouseAction(event, x, y, flags, param):
                if event == cv2.EVENT_FLAG_LBUTTON:
                    pointToMove = (x, y)
                    if self.isMoving == False:
                        self.move(pointToMove);

            self.__setFirstDisplay(mouseAction)

            while (1):
                esc = cv2.waitKey(1)
                if esc == 27: #escape pressed
                    break
            cv2.destroyAllWindows


    def __setFirstDisplay(self, mouseAction):
        img = np.zeros((512, 1000, 3), np.uint8, 'C')
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', mouseAction)
        cv2.rectangle(img, (self.positionX - 20, self.positionY - 20), (self.positionX + 20, self.positionY + 20),
                      (0, 255, 0), -1, 1)
        cv2.imshow('image', img)


robot = RobotMock()









