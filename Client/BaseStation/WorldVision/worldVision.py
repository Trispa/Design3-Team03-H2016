from worldImage import WorldImage
import os
import cv2

class worldVision:

    def __init__(self):
        self.camera = cv2.VideoCapture(1)


    def saveImage(self):

        ret, frame = self.camera.read()

        geometricalImage = WorldImage(frame)

        geometricalImage.setMap()
        geometricalImage.addLabels()

        worldImage = geometricalImage.drawMapOnImage()
        c = os.path.dirname(__file__)
        picturePath = os.path.join(c, "..", "..", "..", "Shared", "worldImage.jpg")
        cv2.imwrite( picturePath, worldImage )
