from Client.BaseStation.WorldVision.worldImage import WorldImage
import os
import base64
from Client.BaseStation.WorldVision.worldVision import worldVision
import cv2


if __name__ == '__main__':

    camera = cv2.VideoCapture(1)
    camera.set(3, 720)
    camera.set(4, 960)
    ret, frame = camera.read()

    #frame = cv2.imread('Photos/3105/table 5/jour/rideau ouvert/Picture 18.jpg')
    #frame = cv2.imread('Images/Test6.jpg')
    geometricalImage = WorldImage(frame)
    #worldVision = worldVision()

    while(True):
        #ret, frame = camera.read()
        frame = cv2.imread('Photo-Test/Frames/Picture 14.jpg')
        geometricalImage = WorldImage(frame)

        geometricalImage.setMap(frame)
        geometricalImage.addLabels(frame)
        worldImage = geometricalImage.drawMapOnImage(frame)
        cv2.imshow("Monde", worldImage)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    #cap.release()
    cv2.destroyAllWindows()
