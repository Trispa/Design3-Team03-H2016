from Client.BaseStation.WorldVision.worldImage import WorldImage
import copy
from Client.BaseStation.WorldVision.worldVision import worldVision
import cv2
import cProfile




def myMain():
    frame = cv2.imread('Photo-Test/Frames/Picture 500.jpg')
    geometricalImage = WorldImage()

    #while(True):

    #ret, frame = camera.read()
    frame = cv2.imread('Photo-Test/Frames/Picture 500.jpg')
    frame = cv2.resize(frame, (960, 720))
    copyF = copy.copy(frame)

    geometricalImage.buildMap(frame)
    geometricalImage.updateRobotPosition(frame)
    geometricalImage.addLabels(frame)
    worldImage = geometricalImage.drawMapOnFrame(frame)
    cv2.imshow("resized", frame)

    #if cv2.waitKey(1) & 0xFF == ord('q'):
        #cv2.imwrite('test.jpg',copyF)
        #break

def myMain2():

    camera = cv2.VideoCapture(1)
    camera.set(3, 3264)
    camera.set(4, 2448)

    frame = cv2.imread('Photo-Test/Frames/Picture 500.jpg')
    geometricalImage = WorldImage()

    while(True):

        #ret, frame = camera.read()
        frame = cv2.imread('Photo-Test/Frames/Picture 500.jpg')
        frame = cv2.resize(frame, (960, 720))
        # copyF = copy.copy(frame)
        geometricalImage.buildMap(frame)
        geometricalImage.updateRobotPosition(frame)
        geometricalImage.addLabels(frame)
        geometricalImage.defineTreasures([30, 150, 87])
        geometricalImage.getIslandPositioning("Square")
        geometricalImage.drawMapOnImage(frame)

        cv2.imshow("resized", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            #cv2.imwrite('test.jpg',copyF)
            break

if __name__ == '__main__':
    myMain2()
    #cProfile.run('myMain()')