from Client.BaseStation.WorldVision.worldImage import WorldImage
import copy
from Client.BaseStation.WorldVision.worldVision import worldVision
import cv2


if __name__ == '__main__':

    #camera = cv2.VideoCapture(0)
    #camera.set(3, 3264)
    #camera.set(4, 2448)

    frame = cv2.imread('Photo-Test/Frames/Picture 177.jpg')
    geometricalImage = WorldImage(frame)

    while(True):

        #ret, frame = camera.read()
        frame = cv2.imread('Photo-Test/Frames/Picture 220.jpg')
        frame = cv2.resize(frame, (960, 720))
        copyF = copy.copy(frame)

        geometricalImage.buildMap(frame)
        geometricalImage.addLabels(frame)
        worldImage = geometricalImage.drawMapOnImage(frame)
        cv2.imshow("resized", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite('test.jpg',copyF)
            break
    camera.release()
    cv2.destroyAllWindows()
