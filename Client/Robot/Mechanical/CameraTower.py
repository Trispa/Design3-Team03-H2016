import time
VERTICAL = 0
HORIZONTALE = 1

class CameraTower:
    def __init__(self, maestro):
        self.maestro = maestro
        self.horizontalDegree = 100
        self.verticalDegree = 30
        self.step = 5
        self.moveCameraByAngle(0, self.verticalDegree)
        self.moveCameraByAngle(1, self.horizontalDegree)

    def moveCameraByAngle(self, direction, angle):
        if direction == 0:
            if angle > 135:
                angle = 135
            self.verticalDegree = self.angleLimit(angle)
            # print("Verticale : " + str(self.degreeVerti))
            self.maestro.setTargetOnMap(direction, self.getPWMfromAngle(angle))
        elif direction == 1:
            self.horizontalDegree = self.angleLimit(angle)
            # print("Horizaontal : " + str(self.degreeHori))
            self.maestro.setTargetOnMap(direction, self.getPWMfromAngle(angle))
        else:
            return -1

    def moveCameraUp(self):
        self.verticalDegree += self.step
        self.moveCameraByAngle(0, self.verticalDegree)

    def moveCameraDown(self):
        self.verticalDegree -= self.step
        self.moveCameraByAngle(0, self.verticalDegree)

    def moveCameraLeft(self):
        self.horizontalDegree -= self.step
        self.moveCameraByAngle(1, self.horizontalDegree)

    def moveCameraRight(self):
        self.horizontalDegree += self.step
        self.moveCameraByAngle(1, self.horizontalDegree)

    def centerCamera(self):
        self.moveCameraByAngle(0, 112)
        self.moveCameraByAngle(1, 121)

    def angleLimit(self, angle):
        angleToVerify = angle
        if angleToVerify < 5:
            return 5
        elif angleToVerify > 174:
            return 174
        else:
            return angleToVerify

    def getPWMfromAngle(self, angle):
        na = 0
        pwm = 0
        if angle < 5:
            na = 5
        elif angle > 174:
            na = 174
        else:
            na = angle
        pwm = (10.293 * na + 626.277) * 4
        return int(pwm)

    def demo(self):
        while(1):
            self.moveCameraByAngle(0, 0)
            self.moveCameraByAngle(1, 0)
            time.sleep(1)
            while self.horizontalDegree < 170:
                self.moveCameraUp()
                self.moveCameraRight()
                time.sleep(0.4)

            self.moveCameraByAngle(0, 100)
            self.moveCameraByAngle(1, 100)
            while self.verticalDegree > 60:
                self.moveCameraLeft()
                self.moveCameraDown()
                time.sleep(0.4)

            self.centerCamera()
            time.sleep(2)


if __name__ == "__main__":
    ct = CameraTower()
    ct.demo()
    time.sleep(2)
    # time.sleep(1)
    # while 1:
    #     ct.moveCameraRight()
    #     time.sleep(0.5)
    ct.maestro.close()
