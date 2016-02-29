from Client.BaseStation.WorldVision.worldImage import WorldImage
import cv2


if __name__ == '__main__':

    cap = cv2.VideoCapture(1)

    while(True):
        #ret, frame = cap.read()
        frame = cv2.imread('Images/Test2.jpg')

        mapImage = WorldImage(frame)
        mapImage.setMap()
        worldImage = mapImage.drawMapOnImage()

        cv2.imwrite( "../../../Commun/worldImage.jpg", worldImage)
        cv2.imshow('frame',worldImage)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

