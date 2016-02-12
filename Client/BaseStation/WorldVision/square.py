from shape import Shape
import numpy as np
import copy

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