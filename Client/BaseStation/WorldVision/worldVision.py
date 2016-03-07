from worldImage import WorldImage
import os
import base64
import cv2

class worldVision:

    def __init__(self):
        self.camera = cv2.VideoCapture(0)


    def saveImage(self):

        ret, frame = self.camera.read()
        geometricalImage = WorldImage(frame)
        geometricalImage.setMap()
        geometricalImage.addLabels()

        worldImage = geometricalImage.drawMapOnImage()


        cnt = cv2.imencode('.png',worldImage)[1]
        b64 = base64.encodestring(cnt)
        #
        # c = os.path.dirname(__file__)

        return b64


