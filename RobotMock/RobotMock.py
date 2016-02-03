import cv2
import numpy as np
import random
import time
import math

#create a full black image (for UI)

class RobotMock:
    deplacement = False
    positionX, positionY = 0, 0
    orientation = 0;

    def __init__(self):
        self.positionX = random.randrange(0,300)
        self.positionY = random.randrange(0,300)


    def move(self, pointToMoveTo):
        self.deplacement = True
        #dans la classe qui serais Mouvement
        deplacementX = pointToMoveTo.__getitem__(0) - self.positionX
        deplacementY = pointToMoveTo.__getitem__(1) - self.positionY
        deplacementTotal = float(abs(deplacementX) +abs(deplacementY))

        #set la vitesse des "roues"
        vitesseX = int(math.ceil(20*(deplacementX/deplacementTotal)))
        vitesseY = int(math.ceil(20*(deplacementY/deplacementTotal)))





        while deplacementX != 0 or deplacementY != 0:
            deplacementX = self.__deplacementX__(deplacementX, vitesseX)
            deplacementY = self.__deplacementY__(deplacementY, vitesseY)


            #trash pour afficher le deplacement
            img = np.zeros((512,1000,3), np.uint8, 'C')
            cv2.namedWindow('image')
            cv2.rectangle(img, (self.positionX - 20, self.positionY - 20), (self.positionX + 20, self.positionY + 20), (0, 255, 0), -1, 1)
            cv2.imshow('image', img)
            cv2.waitKey(1)
            time.sleep(0.05)
        self.deplacement = False

    def __deplacementY__(self, deplacementY, vitesseY):
        if abs(deplacementY) >= abs(vitesseY) and deplacementY != 0 and vitesseY != 0:
            self.positionY += vitesseY
            deplacementY -= vitesseY
        else:
            self.positionY += deplacementY
            deplacementY = 0
        return deplacementY

    def __deplacementX__(self, deplacementX, vitesseX):
        if abs(deplacementX) >= abs(vitesseX) and deplacementX != 0 and vitesseX != 0:
            self.positionX += vitesseX
            deplacementX -= vitesseX
        else:
            self.positionX += deplacementX
            deplacementX = 0
        return deplacementX

#trash pour faire afficher
robot = RobotMock()

def mouseAction(event, x, y, flags, param):
    if event == cv2.EVENT_FLAG_LBUTTON:
        pointToMove = (x,y)
        if robot.deplacement == False:
            robot.move(pointToMove);

img = np.zeros((512,1000,3), np.uint8, 'C')
cv2.namedWindow('image')
cv2.setMouseCallback('image', mouseAction)

cv2.rectangle(img, (robot.positionX - 20, robot.positionY - 20), (robot.positionX + 20, robot.positionY + 20), (0, 255, 0), -1, 1)
cv2.imshow('image', img)

while (1):
    k = cv2.waitKey(1)
    if k == ord('m'):
        mode = not mode
    elif k == 27:
        break
cv2.destroyAllWindows







