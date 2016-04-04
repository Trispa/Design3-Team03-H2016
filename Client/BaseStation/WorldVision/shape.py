import cv2
import numpy as np
from colorContainer import ColorContainer
from Client.BaseStation.WorldVision.Factories.ColorFactory import ColorFactory


class Shape:

    def __init__(self, geometricName, contour):
        self.contour = contour
        self.geometricName = geometricName
        colorFactory = ColorFactory()
        self.color = colorFactory.constructColor(np.uint8([[[0, 255, 255]]]), "Not defined")

    def __eq__(self, other):
        if other == None:
            return False
        return self.contour[0].item(0) == other.contour[0].item(0) and self.contour[0].item(1) == other.contour[0].item(1)

    def getContour(self):
        if len(self.contour) < 2:
            return []
        return self.contour

    def getColorName(self):
        return self.color.getName()

    def getArea(self):
        if len(self.contour) < 3:
            return 0
        return cv2.contourArea(self.contour)

    def getBoundingRectangle(self):
        return cv2.boundingRect(self.contour)

    def getName(self):
        return self.geometricName

    def setColor(self, color):
        self.color = color

    def getCornerCount(self):
        return len(self.contour)

    def getEdgesList(self):
        edgeList = []
        edge = (self.contour[len(self.contour) - 1], self.contour[0])
        edgeList.append(edge)
        for corner in range(0, len(self.contour) - 1):
            edge = (self.contour[corner], self.contour[corner + 1])
            edgeList.append(edge)
        return edgeList

    def findColor(self, frame):
        xCoordinate, yCoordinate, width, height = self.getBoundingRectangle()
        xStart = xCoordinate
        xEnd = xCoordinate + width
        yStart = yCoordinate
        yEnd = yCoordinate + height
        cropped = None
        cropped = frame[yStart:yEnd, xStart:xEnd]
        centerX = cropped.shape[0] / 2
        centerY = cropped.shape[1] / 2
        bgrShapeColor = np.uint8([[[cropped[centerX][centerY][0],cropped[centerX][centerY][1],cropped[centerX][centerY][2]]]])
        hsvShapeColor = cv2.cvtColor(bgrShapeColor,cv2.COLOR_BGR2HSV)
        for color in ColorContainer.colors:
            if color.isInSameColorRange(hsvShapeColor):
                self.color = color

    def findCenterOfMass(self):
        if len(self.contour) > 2:
            moment = cv2.moments(self.contour)
            centerOfMassX = int(moment['m10']/moment['m00'])
            centerOfMassY = int(moment['m01']/moment['m00'])
            return centerOfMassX, centerOfMassY
        else:
            return 0, 0

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

    def isOutsideLimit(self, limit):
        limitMaxX, limitMaxY = limit.getMaxCorner()
        limitMinX, limitMinY = limit.getMinCorner()
        for corner in self.contour:
            if corner.item(1) < limitMinY or corner.item(1) > limitMaxY:
                return True
        return False

<<<<<<< HEAD
    def isOutside(self, point):
        xElementCoordinate,yElementCoordinate,width,height = cv2.boundingRect(self.contour)
        minX = xElementCoordinate
        minY = yElementCoordinate
        maxX = xElementCoordinate + width
        maxY = yElementCoordinate + height
        if point[0] > minX and point[0] < maxX and point[1] > minY and point[1] < maxY:
            return False
        return True

    def asSimilarCenterOfMass(self, otherShape):
        myCenterOfMassX, myCenterOfMassY = self.findCenterOfMass()
        otherShapeCenterOfMassX, otherShapeCenterOfMassY = otherShape.findCenterOfMass()
        if abs(myCenterOfMassX - otherShapeCenterOfMassX) < 10 and abs(myCenterOfMassX - otherShapeCenterOfMassY) < 10:
            return True

        return False


=======
>>>>>>> master




