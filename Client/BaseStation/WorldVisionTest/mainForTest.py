from Client.BaseStation.WorldVision.worldImage import WorldImage
import os
import base64
from Client.BaseStation.WorldVision.worldVision import worldVision
import cv2


if __name__ == '__main__':

    #cap = cv2.VideoCapture(2)

    while(True):
        #ret, frame = cap.read()
        frame = cv2.imread('Photo/3105/table 5/jour/rideau ouvert/Picture 22.jpg')

        geometricalImage = WorldImage(frame)
        geometricalImage.setMap()
        geometricalImage.defineShapesColor()
        geometricalImage.addLabels()
        worldImage = geometricalImage.drawMapOnImage()

        cv2.imshow('frame',frame)
        geometricalImage = WorldImage(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
             break

