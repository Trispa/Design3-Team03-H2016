from worldImage import WorldImage
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
        cv2.imwrite( "../../Shared/worldImage.jpg", worldImage )
