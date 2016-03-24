import math

class Robot():
    def __init__(self, square, circle):
        self.square = square
        self.circle = circle
        self.orientation = 0

    def setOrientation(self):
        if len(self.circle.getContour()) > 2 and len(self.square.getContour()) > 2:
            origin = self.circle.findCenterOfMass()
            end = self.square.findCenterOfMass()
            x = float(end[0] - origin[0])
            y = float(end[1] - origin[1])
            if(x == 0):
                if(y >= 0):
                    angle = 90.0
                else:
                    angle = 270.0
            else:
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
        else:
            self.orientation = 0
