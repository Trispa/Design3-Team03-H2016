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

    def __eq__(self, other):
        if other == None:
            return False
        return cv2.contourArea(self.contour) == cv2.contourArea(other.contour)

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

    def getArea(self):
        return cv2.contourArea(self.contour)

    def getBoundingRectangle(self):
        return cv2.boundingRect(self.contour)

    def getName(self):
        return self.geometricName

    def asSimilarCenterOfMass(self, otherShape):
        myCenterOfMassX, myCenterOfMassY = self.findCenterOfMass()
        otherShapeCenterOfMassX, otherShapeCenterOfMassY = otherShape.findCenterOfMass()
        if abs(myCenterOfMassX - otherShapeCenterOfMassX) < 10 and abs(myCenterOfMassX - otherShapeCenterOfMassY) < 10:
            return True

        return False

    def angle_cos(p0, p1, p2):
        d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
        return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )


