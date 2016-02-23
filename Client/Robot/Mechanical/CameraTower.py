import time
import maestro
#Class CameraTower : permet de bouger la camera embarque
class CameraTower:
    def __init__(self):
        self.maestro = maestro.Controller()
        self.step = 10
        self.degreeHori = 90
        self.degreeVerti = 90
        self.servoHori = 0
        self.servoVerti = 1
        self.writeCameraByAngleHori(self.degreeHori)
        self.writeCameraByAngleVerti(self.degreeVerti)

    #Place le monteur Horizontalea l'angle entre en parametre
    def writeCameraByAngleHori(self, degree):
        self.degreeHori = self.angleLimit(degree)
        pwm = self.degreeToPWM(self.degreeHori)
        self.maestro.setTarget(0, pwm)
    #Place le moteut Verticale a l'angle entre en parametre
    def writeCameraByAngleVerti(self, degree):
        self.degreeVerti = self.angleLimit(degree)
        if self.degreeVerti > 125:
            self.degreeVerti = 125
        pwm = self.degreeToPWM(self.degreeVerti)
        self.maestro.setTarget(1, pwm)

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

    def degreeToPWM(self, d):
        if(d is not None):
            return int(17.2 * d - 500 * 4)
        else:
            return 0


if __name__ == "__main__":

    c = CameraTower()
    c.step = 20

    c.writeCameraByAngleHori(170)
    c.writeCameraByAngleVerti(90)
    time.sleep(2)

    # i = -1
    # while(1):
    # #     print("Dans la boucle while : " + str(i))
    # #     # c.servoVerti.write(i)
    # #     # i = i+5
    # #     # if(i > 186):
    # #     #     i = 0
    # #     # time.sleep(1)
    # #
    # #
    # #
    #     c.moveCameraDown()
    #     time.sleep(1)
    #     c.moveCameraDownByAngle(30)
    #     print("Down")
    #     time.sleep(1)
    #     c.moveCameraLeft()
    #     time.sleep(1)
    #     c.moveCameraLeftByAngle(60)
    #     time.sleep(1)
    #     print("Left")
    #     c.moveCameraRight()
    #     time.sleep(1)
    #     c.moveCameraRightByAngle(60)
    #     time.sleep(1)
    #     print("Right")
    #     c.moveCameraUp()
    #     time.sleep(1)
    #     c.moveCameraUpByAngle(30)
    #     time.sleep(1)
    #     print("Up")

        # c.writeCameraByAngleHori(0)
        # c.writeCameraByAngleVerti(0)
        # time.sleep(2)
        # c.writeCameraByAngleHori(90)
        # c.writeCameraByAngleVerti(90)
        # time.sleep(2)
        # c.writeCameraByAngleVerti(180)
        # c.writeCameraByAngleHori(180)
        # time.sleep(2)
