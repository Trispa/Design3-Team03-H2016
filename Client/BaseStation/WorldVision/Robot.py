import math

class Robot():
    def __init__(self, square, circle):
        self.square = square
        self.circle = circle
        self.orientation = 0

    def setOrientation(self):
        origin = self.circle.findCenterOfMass()
        end = self.square.findCenterOfMass()
        x = float(end[0] - origin[0])
        y = float(end[1] - origin[1])

        angle = abs(math.degrees(math.atan(y/x)))
        if(x >= 0 and y < 0):
            angle = 360 - angle
        elif(x>=0 and y >= 0):
            angle = angle
        elif(x < 0 and y < 0):
            angle = angle + 180
        elif(x < 0 and y >= 0):
            angle = 180 - angle

        self.orientation = angle
