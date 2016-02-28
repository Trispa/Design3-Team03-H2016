from Client.BaseStation.WorldVision.worldImage import WorldImage
import cv2


if __name__ == '__main__':

    cap = cv2.VideoCapture(1)

    ret, frame = cap.read()

    geometricalImage = WorldImage(frame)
    geometricalImage.setMap()
    print(geometricalImage.getMap().getShapesList()[0])
    geometricalImage.addLabels()

    worldImage = geometricalImage.drawMapOnImage()
    cv2.imwrite( "../../../Shared/worldImage.jpg", worldImage )

    ret, frame = cap.read()

    geometricalImage = WorldImage(frame)
    geometricalImage.setMap("GeometricalFilter")
    geometricalImage.addLabels()

    worldImage = geometricalImage.drawMapOnImage()
    cv2.imwrite( "../../../Shared/worldImage2.jpg", worldImage )

