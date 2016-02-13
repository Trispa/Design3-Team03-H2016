import cv2
import numpy as np

class Shape:

    def __init__(self, geometricName, contour):
        self.contour = contour
        self.geometricName = geometricName

    def findCenterOfMass(self):
        moment = cv2.moments(self.contour)
        centerOfMassX = int(moment['m10']/moment['m00'])
        centerOfMassY = int(moment['m01']/moment['m00'])
        return centerOfMassX, centerOfMassY

    def isEqualEdges(self):
        arbitraryEdge = np.array([self.contour[0], self.contour[1]])
        arbitraryNormalLength = cv2.arcLength(arbitraryEdge, False)
        print(arbitraryNormalLength)
        for corner in range(1 , len(self.contour) - 1):
            length = cv2.arcLength(np.array([self.contour[corner], self.contour[corner + 1]]), False)
            if abs(length - arbitraryNormalLength) > 20:
                return False

        return True

    def checkAngleValue(self):
        return True

    def getContour(self):
        return self.contour

    def getBoudingRectangle(self):
        return cv2.boundingRect(self.contour)

    def getName(self):
        return self.geometricName

    def angle_cos(p0, p1, p2):
        d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
        return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

