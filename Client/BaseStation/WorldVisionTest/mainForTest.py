from Client.BaseStation.WorldVision.worldImage import WorldImage
import cv2


if __name__ == '__main__':

    cap = cv2.VideoCapture(0)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        #frame = cv2.imread("Images/Test3.jpg")

        geometricalImage = WorldImage(frame)
        geometricalImage.setMap()
        geometricalImage.addLabels()

        worldImage = geometricalImage.drawMapOnImage()

        cv2.imshow('frame', worldImage)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

