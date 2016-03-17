import cv2
import copy
import numpy as np



class Robot():
    def __init__(self, square):
        self.square = square

    def setOrientationCircle(self, circle):
        self.circle = circle


    def Slope(self, startX, startY, endX, endY):
        return (endY - startY) / (endX - startX)


    def fullLine(self, image, startPoint, endPoint):
        if(endPoint[0] - startPoint[0] != 0 and endPoint[1] - startPoint[1] != 0):
            #green
            curve = self.Slope(startPoint[0], startPoint[1], endPoint[0], endPoint[1])

            imageBorderStart = (0, -(startPoint[0]) * curve + startPoint[1])
            imageBorderEnd = (image.shape[1], -(endPoint[0] - image.shape[1]) * curve + endPoint[1])

            cv2.line(image, imageBorderStart, imageBorderEnd, (0, 255, 0), 5)


        elif(endPoint[0] - startPoint[0]):
            #red
            imageBorderStart = (0, startPoint[1])
            imageBorderEnd = (image.shape[1], endPoint[1])

            cv2.line(image, imageBorderStart, imageBorderEnd, (0, 255, 0), 5)

        elif(endPoint[1] - startPoint[1]):
            #blue
            imageBorderStart = (startPoint[0], 0)
            imageBorderEnd = (endPoint[0], image.shape[1])

            cv2.line(image, imageBorderStart, imageBorderEnd, (0, 255, 0), 5)


    def setOrientation(self, mapImage):
        image = copy.copy(mapImage)

        self.fullLine(image, self.square.findCenterOfMass(), self.circle.findCenterOfMass())
        self.fullLine(image, self.circle.findCenterOfMass(), (self.circle.findCenterOfMass()[0], 0))
        self.fullLine(image, self.circle.findCenterOfMass(), (0, self.circle.findCenterOfMass()[1]))
        self.fullLine(image, (0,100), (30,100))
        self.fullLine(image, (0,590), (30,590))

        cv2.imshow("foo",image)
        cv2.waitKey()
