from Client.BaseStation.WorldVision.worldImage import WorldImage
import copy
import cv2
from Client.BaseStation.Logic.TargetTypes import ShapeTarget
import cProfile




def myMain():
    #frame = cv2.imread('Photo-Test/Frames/Picture 500.jpg')
    geometricalImage = WorldImage()

    camera = cv2.VideoCapture(1)

    while(True):

        ret, frame = camera.read()
        #frame = cv2.imread('Photo-Test/Frames/Picture 500.jpg')
        frame = cv2.resize(frame, (960, 720))
        copyF = copy.copy(frame)

        geometricalImage.buildMap(frame)
        geometricalImage.updateRobotPosition(frame)
        geometricalImage.addLabels(frame)
        worldImage = geometricalImage.drawMapOnFrame(frame)
        cv2.imshow("resized", worldImage)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def myMain2():

    camera = cv2.VideoCapture(0)
    camera.set(3, 3264)
    camera.set(4, 2448)

    #frame = cv2.imread('Photo-Test/Frames/Picture 500.jpg')
    geometricalImage = WorldImage()

    while(True):


        #ret, frame = camera.read()
        frame = cv2.imread('Photo-Test/Frames/Picture 500.jpg')
        frame = cv2.resize(frame, (960, 720))
        # copyF = copy.copy(frame)
        geometricalImage.buildMap(frame)
        geometricalImage.updateRobotPosition(frame)
        geometricalImage.defineTreasures([88, 30])
        geometricalImage.findBestTresor()
        geometricalImage.addLabels(frame)
        geometricalImage.defineTreasures([30, 150, 87])
        myTarget = ShapeTarget("triangle")
        geometricalImage.getIslandPositioning(myTarget)

        geometricalImage.drawMapOnFrame(frame)


        cv2.imshow("resized", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            #cv2.imwrite('test.jpg',copyF)
            break

if __name__ == '__main__':
    myMain()
    #cProfile.run('myMain()')