from Client.BaseStation.WorldVision.worldImage import WorldImage
import os
import base64
from Client.BaseStation.WorldVision.worldVision import worldVision
import cv2


if __name__ == '__main__':

    camera = cv2.VideoCapture(0)
    #worldVision = worldVision()

    while(True):
        #ret, frame = cap.read()
        #frame = cv2.imread('Images/Test6.jpg')


        ret, frame = camera.read()
        geometricalImage = WorldImage(frame)
        geometricalImage.setMap()
        geometricalImage.addLabels()

        worldImage = geometricalImage.drawMapOnImage()


        # geometricalImage = WorldImage(frame)
        # geometricalImage.setMap()
        # geometricalImage.defineShapesColor()
        # geometricalImage.addLabels()
        # worldImage = geometricalImage.drawMapOnImage()

        # geometricalImage = WorldImage(frame)
        # geometricalImage.setMap()
        # geometricalImage.addLabels()
        # worldImage = geometricalImage.drawMapOnImage()


    #cap.release()
    cv2.destroyAllWindows()

