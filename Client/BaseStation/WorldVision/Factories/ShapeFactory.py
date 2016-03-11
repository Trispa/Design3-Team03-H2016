from Client.BaseStation.WorldVision.allShapes import *

class ShapeFactory():
    def ConstructShape(self, contours):
        if len(contours) == 3:
            return Triangle("Triangle", contours)
        elif len(contours) == 4:
            return Square("Square", contours)
        elif len(contours) == 5:
            return Shape("Pentagone", contours)
        elif len(contours) > 5:
            return Shape("Circle", contours)