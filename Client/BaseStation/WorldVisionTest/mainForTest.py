from Client.BaseStation.WorldVision.worldImage import WorldImage
import os
import cv2


if __name__ == '__main__':

    cap = cv2.VideoCapture(0)

#while(True):
    #ret, frame = cap.read()
    frame = cv2.imread('Images/Test1.jpg')

    geometricalImage = WorldImage(frame)
    geometricalImage.setMap()
    geometricalImage.defineShapesColor()
    geometricalImage.addLabels()
    worldImage = geometricalImage.drawMapOnImage()

    cv2.imwrite( "../../../Shared/worldImage.jpg", worldImage)
    cv2.imshow('frame',frame)
    cv2.waitKey(0)
    #if cv2.waitKey(1) & 0xFF == ord('q'):
        #break

cap.release()
cv2.destroyAllWindows()

