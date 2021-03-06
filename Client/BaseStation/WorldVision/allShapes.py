from shape import Shape
import numpy as np
import copy
import math

class Square(Shape):

    def __init__(self, geometricName, contour):
        Shape.__init__(self, geometricName, contour)
        cornerList = []
        self.minX = 1000
        self.maxX = 0
        self.minY = 1000
        self.maxY = 0
        contourCopy = contour
        if len(contourCopy) > 1:
            for corner in contourCopy:
                cornerList.append((corner.item(0), corner.item(1)))
            for corner in cornerList:
                if(corner[0] > self.maxX):
                    self.maxX = corner[0]
                if(corner[1] > self.maxY):
                    self.maxY = corner[1]
                if(corner[0] < self.minX):
                    self.minX = corner[0]
                if(corner[1] < self.minY):
                    self.minY = corner[1]
        else:
            self.minX = 0
            self.maxX = 960
            self.minY = 0
            self.maxY = 720

    def __angleCos(self, p0, p1, p2):
        d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
        return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

    def checkAngleValue(self):
        cntCopy = copy.copy(self.contour)
        cntCopy = cntCopy.reshape(-1, 2)
        max_cos = np.max([self.__angleCos( cntCopy[i], cntCopy[(i+1) % 4], cntCopy[(i+2) % 4] ) for i in xrange(4)])
        if max_cos < 0.1:
            return True

    def getMaxCorner(self):
        return self.maxX, self.maxY

    def getMinCorner(self):
        return self.minX, self.minY

class Triangle(Shape):

    def __init__(self, geometricName, contour):
        Shape.__init__(self, geometricName, contour)

    def __getAngle(self, vector1, vector2):
        dot = vector1[0]*vector2[0] + vector1[1]*vector2[1]
        x_modulus = np.sqrt((vector1[0]*vector1[0]) + (vector1[1]*vector1[1]))
        y_modulus = np.sqrt((vector2[0]*vector2[0]) + (vector2[1]*vector2[1]))
        cos_angle = dot / x_modulus / y_modulus
        angle = np.arccos(cos_angle)
        angleInDegree = (angle * 360 / 2 / np.pi)
        return abs(angleInDegree - 180)

    def checkAngleValue(self):
        vectorList = []
        for point in range(0, len(self.contour) - 1):
            vectorList.append(self.__getVector(np.array([self.contour[point], self.contour[point + 1]]).tolist()))

        vectorList.append(self.__getVector(np.array([self.contour[2], self.contour[0]]).tolist()))

        angleList = []
        angleList.append(self.__getAngle(vectorList[2], vectorList[0]))
        for vector in range(0, len(vectorList) - 1):
            angleList.append(self.__getAngle(vectorList[vector], vectorList[vector + 1]))

        totalAngleInPolygone = ((len(self.contour) - 2) * 180)/len(self.contour)
        maxAngle = totalAngleInPolygone + 15
        minAngle = totalAngleInPolygone - 15
        for angle in angleList:
            if angle > maxAngle or angle < minAngle:
                return False

        return True

    def __getVector(self, specialArray):
        newArray = [specialArray[1][0][0] - specialArray[0][0][0], specialArray[1][0][1] - specialArray[0][0][1]]
        return newArray

