import cv2
import numpy as np
from color import Color

class Shape:

    colors = []
    colors.append(Color(np.uint8([[[0,255,0]]]), "Green"))
    colors.append(Color(np.uint8([[[255,0,0]]]), "Blue"))
    colors.append(Color(np.uint8([[[150,179,255]]]), "Red"))
    colors.append(Color(np.uint8([[[0,255,255]]]), "Yellow"))

    def __init__(self, geometricName, contour):
        self.contour = contour
        self.geometricName = geometricName
        self.myColor = Color(np.uint8([[[0,255,255]]]), "Not defined")


    def __eq__(self, other):
        if other == None:
            return False
        return self.contour[0].item(0) == other.contour[0].item(0)

    def findCenterOfMass(self):
        moment = cv2.moments(self.contour)
        centerOfMassX = int(moment['m10']/moment['m00'])
        centerOfMassY = int(moment['m01']/moment['m00'])
        return centerOfMassX, centerOfMassY

    def isEqualEdges(self):
        arbitraryEdge = np.array([self.contour[0], self.contour[1]])
        arbitraryNormalLength = cv2.arcLength(arbitraryEdge, False)
        for corner in range(1 , len(self.contour) - 1):
            length = cv2.arcLength(np.array([self.contour[corner], self.contour[corner + 1]]), False)
            if abs(length - arbitraryNormalLength) > 10:
                return False

        return True

    def checkAngleValue(self):
        return True

    def getContour(self):
        return self.contour

    def getColorName(self):
        return "colorName"

    def getArea(self):
        return cv2.contourArea(self.contour)

    def getBoundingRectangle(self):
        return cv2.boundingRect(self.contour)

    def getName(self):
        return self.geometricName

    def getColor(self):
        return self.myColor

    def getCornerCount(self):
        return len(self.contour)

    def isOutside(self, limit):
        limitMaxX, limitMaxY = limit.getMaxCorner()
        limitMinX, limitMinY = limit.getMinCorner()
        for corner in self.contour:
            if corner.item(1) < limitMinY or corner.item(1) > limitMaxY:
                return True
        return False

    def asSimilarCenterOfMass(self, otherShape):
        myCenterOfMassX, myCenterOfMassY = self.findCenterOfMass()
        otherShapeCenterOfMassX, otherShapeCenterOfMassY = otherShape.findCenterOfMass()
        if abs(myCenterOfMassX - otherShapeCenterOfMassX) < 10 and abs(myCenterOfMassX - otherShapeCenterOfMassY) < 10:
            return True

        return False


    def setColor(self, mapImage):
        xCoordinate, yCoordinate, width, height = self.getBoundingRectangle()
        xStart = xCoordinate
        xEnd = xCoordinate + width
        yStart = yCoordinate
        yEnd = yCoordinate + height
        cropped = None
        cropped = mapImage[yStart:yEnd, xStart:xEnd]
        centerX = cropped.shape[0] / 2
        centerY = cropped.shape[1] / 2
        bgrShapeColor = np.uint8([[[cropped[centerX][centerY][0],cropped[centerX][centerY][1],cropped[centerX][centerY][2]]]])
        hsvShapeColor = cv2.cvtColor(bgrShapeColor,cv2.COLOR_BGR2HSV)
        for color in self.colors:
            if color.isInSameColorRange(hsvShapeColor):
                self.myColor = color



