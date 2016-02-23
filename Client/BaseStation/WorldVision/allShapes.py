from shape import Shape
import numpy as np
import copy
import math

class Square(Shape):

    def __init__(self, geometricName, contour):
        Shape.__init__(self, geometricName, contour)

    def __angleCos(self, p0, p1, p2):
        d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
        return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

    def checkAngleValue(self):
        cntCopy = copy.copy(self.contour)
        cntCopy = cntCopy.reshape(-1, 2)
        max_cos = np.max([self.__angleCos( cntCopy[i], cntCopy[(i+1) % 4], cntCopy[(i+2) % 4] ) for i in xrange(4)])
        if max_cos < 0.1:
            return True

#TODO
class Triangle(Shape):

    def __length(self, vector):
        return math.sqrt(np.dot(vector, vector))

    def __angle(self, vector1, vector2):
        dot = np.dot(vector1,vector2)
        x_modulus = np.sqrt((vector1*vector1).sum())
        y_modulus = np.sqrt((vector2*vector2).sum())
        cos_angle = dot / x_modulus / y_modulus # cosine of angle between x and y
        angle = np.arccos(cos_angle)
        return angle * 360 / 2 / np.pi # angle in degrees

    def __init__(self, geometricName, contour):
        Shape.__init__(self, geometricName, contour)

    def checkAngleValue(self):
        vectorList = []
        vectorList.append(np.array([self.contour[0], self.contour[1]]))
        vectorList.append(np.array([self.contour[1], self.contour[2]]))
        vectorList.append(np.array([self.contour[2], self.contour[0]]))

        angleList = []
        angleList.append(self.__angle(vectorList[2], vectorList[0]))
        for vector in range(0, len(vectorList) - 1):
            angleList.append(self.__angle(vectorList[vector], vectorList[vector + 1]))

        for angle in angleList:
            if angle > 65 or angle < 55:
                return False

        return True

