<<<<<<< HEAD
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
            print("Verticale : " + str(self.degreeVerti))
            self.m.setTarget(direction, self.getPWMfromAngle(angle))
        elif direction == 1:
            self.degreeHori = self.angleLimit(angle)
            print("Horizaontal : " + str(self.degreeHori))
            self.m.setTarget(direction, self.getPWMfromAngle(angle))
        else:
            return -1

    def moveCameraUp(self):
        self.degreeVerti += self.step
        self.moveCameraByAngle(0, self.degreeVerti)

    def moveCameraDown(self):
        self.degreeVerti -= self.step
        self.moveCameraByAngle(0, self.degreeVerti)

    def moveCameraLeft(self):
        self.degreeHori -= self.step
        self.moveCameraByAngle(1, self.degreeHori)

    def moveCameraRight(self):
        self.degreeHori += self.step
        self.moveCameraByAngle(1, self.degreeHori)

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
=======
from nanpy import ArduinoApi, SerialManager, Servo
import time

#Class CameraTower : permet de bouger la camera embarque a l'aide de l'arduino
class CameraTower:
    #Le moteur horizontale dans le i/o -- 12 --
    #Le moteur verticale   dans le i/o -- 11 --
    #Step par default = 10 degre
    def __init__(self):
        self.step = 10
        self.degreeHori = 90
        self.degreeVerti = 90
        self.servoHori = Servo(12)
        self.servoVerti = Servo(11)
        self.writeCameraByAngleHori(self.degreeHori)
        self.writeCameraByAngleVerti(self.degreeVerti)

    #Place le monteur Horizontalea l'angle entre en parametre
    def writeCameraByAngleHori(self, degree):
        self.degreeHori = self.angleLimit(degree)
        self.servoHori.write(self.degreeHori)
    #Place le moteut Verticale a l'angle entre en parametre
    def writeCameraByAngleVerti(self, degree):
        self.degreeVerti = self.angleLimit(degree)
        if self.degreeVerti > 125:
            self.degreeVerti = 125
        self.servoVerti.write(self.degreeVerti)

    #Bouge la camera vers le haut de l'angle actuel + self.step (valeur par defaut = 10)
    def moveCameraUp(self):
        self.writeCameraByAngleVerti(self.degreeVerti + self.step)

    #Bouge la camera vers le haut de l'angle actuel + angle (entre en parametre)
    def moveCameraUpByAngle(self, angle):
        self.writeCameraByAngleVerti(self.degreeVerti + angle)

    def moveCameraDown(self):
        self.writeCameraByAngleVerti(self.degreeVerti - self.step)

    def moveCameraDownByAngle(self, angle):
        self.writeCameraByAngleVerti(self.degreeVerti - angle)

    def moveCameraLeft(self):
        self.writeCameraByAngleHori(self.degreeHori - self.step)

    def moveCameraLeftByAngle(self, angle):
        self.writeCameraByAngleHori(self.degreeHori - angle)

    def moveCameraRight(self):
        self.writeCameraByAngleHori(self.degreeHori + self.step)

    def moveCameraRightByAngle(self, angle):
        self.writeCameraByAngleHori(self.degreeHori + angle)

    #Protection de l'angle ecrit dans les servo moteur 2 < angle < 178
    def angleLimit(self, a):
        if(a < 2):
            return 2
        elif(a > 178):
            return 178
        else:
            return a


if __name__ == "__main__":
    # connection = SerialManager(device="/dev/ttyUSB0")
    # a = ArduinoApi(connection=connection)
    # a.pinMode(13, a.OUTPUT)
    # a.digitalWrite(13, a.HIGH)

    c = CameraTower()
    c.step = 20

    c.writeCameraByAngleHori(90)
    c.writeCameraByAngleVerti(90)
    time.sleep(2)

    i = -1
    while(1):
        print("Dans la boucle while : " + str(i))
        # c.servoVerti.write(i)
        # i = i+5
        # if(i > 186):
        #     i = 0
        # time.sleep(1)



        c.moveCameraDown()
        time.sleep(1)
        c.moveCameraDownByAngle(30)
        print("Down")
        time.sleep(1)
        c.moveCameraLeft()
        time.sleep(1)
        c.moveCameraLeftByAngle(60)
        time.sleep(1)
        print("Left")
        c.moveCameraRight()
        time.sleep(1)
        c.moveCameraRightByAngle(60)
        time.sleep(1)
        print("Right")
        c.moveCameraUp()
        time.sleep(1)
        c.moveCameraUpByAngle(30)
        time.sleep(1)
        print("Up")

        # c.writeCameraByAngleHori(0)
        # c.writeCameraByAngleVerti(0)
        # time.sleep(2)
        # c.writeCameraByAngleHori(90)
        # c.writeCameraByAngleVerti(90)
        # time.sleep(2)
        # c.writeCameraByAngleVerti(180)
        # c.writeCameraByAngleHori(180)
        # time.sleep(2)
>>>>>>> 78062ee91767dca66298eff591d85e1a5849e1f0
