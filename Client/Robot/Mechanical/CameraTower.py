import time
import maestro
VERTICAL = 0
HORIZONTALE = 1

class CameraTower:
    def __init__(self):
        self.m = maestro.Controller()
        self.degreeHori = 121
        self.degreeVerti = 112
        self.step = 5
        self.moveCameraByAngle(0, self.degreeVerti)
        self.moveCameraByAngle(1, self.degreeHori)

    def moveCameraByAngle(self, direction, angle):
        if direction == 0:
            if angle > 135:
                angle = 135
            self.degreeVerti = self.angleLimit(angle)
            # print("Verticale : " + str(self.degreeVerti))
            self.m.setTarget(direction, self.getPWMfromAngle(angle))
        elif direction == 1:
            self.degreeHori = self.angleLimit(angle)
            # print("Horizaontal : " + str(self.degreeHori))
            self.m.setTarget(direction, self.getPWMfromAngle(angle))
        else:
            return -1

    def moveCameraUp(self):
        self.degreeVerti += self.step
        self.moveCameraByAngle(0, self.degreeVerti)
        return self.degreeVerti

    def moveCameraDown(self):
        self.degreeVerti -= self.step
        self.moveCameraByAngle(0, self.degreeVerti)
        return self.degreeVerti

    def moveCameraLeft(self):
        self.degreeHori -= self.step
        self.moveCameraByAngle(1, self.degreeHori)
        return self.degreeHori

    def moveCameraRight(self):
        self.degreeHori += self.step
        self.moveCameraByAngle(1, self.degreeHori)
        return self.degreeHori

    def centerCamera(self):
        self.moveCameraByAngle(0, 112)
        self.moveCameraByAngle(1, 121)

    def angleLimit(self, b):
        a = b
        if a < 50:
            return 50
        elif a > 174:
            return 174
        else:
            return a

    def getPWMfromAngle(self, a):
        na = 0
        pwm = 0
        if a < 51:
            na = 51
        elif a > 174:
            na = 174
        else:
            na = a
        pwm = ((17.6 * na) - 573) * 4
        return int(pwm)

    def demo(self):
        while(1):
            self.moveCameraByAngle(0, 0)
            self.moveCameraByAngle(1, 0)
            time.sleep(1)
            while self.degreeHori < 170:
                self.moveCameraUp()
                self.moveCameraRight()
                time.sleep(0.4)

            self.moveCameraByAngle(0, 100)
            self.moveCameraByAngle(1, 100)
            while self.degreeVerti > 60:
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
    ct.m.close()
