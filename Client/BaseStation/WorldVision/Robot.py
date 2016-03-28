import math

class Robot():
    def __init__(self, blackCircle, purpleCircle):
        self.blackCircle = blackCircle
        self.purpleCircle = purpleCircle
        self.orientation = 0
        self.center = (0,0)

    def setOrientation(self):
        if len(self.purpleCircle.getContour()) > 2 and len(self.purpleCircle.getContour()) > 2:
            origin = self.blackCircle.findCenterOfMass()
            end = self.purpleCircle.findCenterOfMass()
            x = float(end[0] - origin[0])
            y = float(end[1] - origin[1])
            if(x == 0):
                if(y >= 0):
                    angle = 135.0
                else:
                    angle = 315.0
            else:
                angle = abs(math.degrees(math.atan(y/x)))
                if(x >= 0 and y < 0):
                    angle = 360 - angle + 45
                    if(angle > 360):
                        angle = 0 + (angle - 360)
                elif(x>=0 and y >= 0):
                    angle = angle + 45
                    if(angle > 90):
                        angle = 90 + (angle - 90)
                elif(x < 0 and y < 0):
                    angle = angle + 180 + 45
                    if(angle > 270):
                        angle = 270 + (angle - 270)
                elif(x < 0 and y >= 0):
                    angle = 180 - angle + 45
                    if(angle > 180):
                        angle = 180 + (angle - 180)

            self.orientation = angle
        else:
            self.orientation = 0

    def setCenter(self):
        origin = self.blackCircle.findCenterOfMass()
        end = self.purpleCircle.findCenterOfMass()
        x = float(end[0] - origin[0])
        y = float(end[1] - origin[1])
        self.center = (origin[0] + x/2, origin[1] + y/2)

