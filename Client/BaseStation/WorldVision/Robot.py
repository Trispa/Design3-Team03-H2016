import cv2
import copy
import numpy as np



class Robot():
    def __init__(self, square):
        self.square = square

    def setOrientationCircle(self, circle):
        self.circle = circle

    def setOrientation(self, mapImage):
        image = copy.copy(mapImage)
        x1, x2, y1, y2 = self.circle.findCenterOfMass()[0], self.square.findCenterOfMass()[0],\
                         self.circle.findCenterOfMass()[1], self.square.findCenterOfMass()[1]

        def line_eq(X):
            m = (y2 - y1) / (x2 - x1)
            return m * (X - x1) + y1

        line = np.vectorize(line_eq)

        x = np.arange(0, 1200)
        y = line(x).astype(np.uint)

        cv2.line(image, (x[0], y[0]), (x[-1], y[-1]), (0,0,0))
        cv2.imshow("foo",image)
        cv2.waitKey()
