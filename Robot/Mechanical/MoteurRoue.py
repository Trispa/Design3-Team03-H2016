from nanpy import ArduinoApi, SerialManager, Servo
import time
import maestro
import Arduino

class MoteurRoue:
    def __init__(self, arduino):
        self.maestroPWM = maestro.Controller()
        self.arduino = arduino

        # connection = SerialManager(device='/dev/ttyUSB0')
        # self.arduino = ArduinoApi(connection=connection)

        #Dictionnaire du mapping des pin dicrection moteur
        self.pinMapping = {'Pin1Motor1': 46, 'Pin2Motor1': 47, 'Pin1Motor2': 48, 'Pin2Motor2': 49, 'Pin1Motor3': 50,
                           'Pin2Motor3': 51, 'Pin1Motor4': 52, 'Pin2Motor4': 53}
        for value in self.pinMapping.values():
            self.arduino.pinMode(value, self.arduino.OUTPUT)
            self.arduino.digitalWrite(value, self.arduino.LOW)

    # clockDirection peut etre CCW ou CW (clockwise, counter clockwise)
    # PWM entre 996 et 3280
    # NoMoteur 1, 2, 3, 4
    def runASpecificWheelByPWM(self, noMotor, clockDirection, pwm):
        if clockDirection == "CW":
            self.arduino.digitalWrite(self.pinMapping.get('Pin1Motor' + str(noMotor)), self.arduino.LOW)
            self.arduino.digitalWrite(self.pinMapping.get('Pin2Motor' + str(noMotor)), self.arduino.HIGH)

        elif clockDirection == "CCW":
            self.arduino.digitalWrite(self.pinMapping.get('Pin1Motor' + str(noMotor)), self.arduino.HIGH)
            self.arduino.digitalWrite(self.pinMapping.get('Pin2Motor' + str(noMotor)), self.arduino.LOW)

        else:
            raise ValueError("La direction doit etre CW ou CCW!!!")

        self.maestroPWM.setTarget(noMotor - 1, 4 * int(self.speedLimiteByPWM(pwm)))

    #Min speed : 0.0737
    #Max speed : 1.0782
    def runASpecificWheelBySpeed(self, noMotor, clockDirection, speed):
        PWM = (speed + 0.07939)/0.00009634
        self.runASpecificWheelByPWM(noMotor, clockDirection, PWM)

    def stopAllMotors(self):
        for value in self.pinMapping.values():
            self.arduino.digitalWrite(value, self.arduino.LOW)

    def stopMotorByNo(self, noMotor):
        self.arduino.digitalWrite(self.pinMapping.get('Pin1Motor' + str(noMotor)), self.arduino.LOW)
        self.arduino.digitalWrite(self.pinMapping.get('Pin2Motor' + str(noMotor)), self.arduino.LOW)

    def reculer(self):
        self.runASpecificWheelByPWM(3, 'CW', 3280)
        self.runASpecificWheelByPWM(2, 'CCW', 3280)

    def avancer(self):
        self.runASpecificWheelByPWM(3, 'CCW', 3280)
        self.runASpecificWheelByPWM(2, 'CW', 3280)

    def rotationCW(self):
        m.runASpecificWheelByPWM(1, 'CCW', 3000)
        m.runASpecificWheelByPWM(2, 'CCW', 3000)
        m.runASpecificWheelByPWM(3, 'CCW', 3000)
        m.runASpecificWheelByPWM(4, 'CCW', 3000)

    def roatationCCW(self):
        m.runASpecificWheelByPWM(1, 'CW', 3000)
        m.runASpecificWheelByPWM(2, 'CW', 3000)
        m.runASpecificWheelByPWM(3, 'CW', 3000)
        m.runASpecificWheelByPWM(4, 'CW', 3000)




    def speedLimiteByPWM(self, pwm):
        if pwm > 3280:
            return 3280
        elif pwm < 996:
            return 996
        else:
            return pwm


if __name__ == '__main__':
    m = MoteurRoue(Arduino.Arduino().a)
    print("Starting script MoteurRoue.py")
    # m.runASpecificWheelBySpeed(1, 'CCW', 0.08)
    # time.sleep(5)
    # m.runASpecificWheelBySpeed(1, 'CW', 0.9)
    # time.sleep(5)
    # m.stopMotorByNo(1)
    # time.sleep(3)
    # m.runASpecificWheelBySpeed(1, 'CW', 0.567)
    # time.sleep(5)
    # i = 0.07
    # while(i <= 1):
    #     m.runASpecificWheelBySpeed(1, 'CCW', i)
    #     print("Speed : " + str(i))
    #     i += 0.05
    #     time.sleep(1)
    # m.runASpecificWheelByPWM(1, 'CCW', 3280)
    # time.sleep(3)


    m.reculer()
    time.sleep(4)
    m.avancer()
    time.sleep(4)
    m.roatationCCW()
    time.sleep(2)
    m.rotationCW()
    time.sleep(2)

    # m.runASpecificWheelByPWM(1, 'CW', 2000)
    # time.sleep(2)
    # m.runASpecificWheelByPWM(2, 'CW', 2000)
    # time.sleep(2)
    # m.runASpecificWheelByPWM(3, 'CW', 2000)
    # time.sleep(2)
    # m.runASpecificWheelByPWM(4, 'CW', 2000)
    # time.sleep(5)
    # m.runASpecificWheelByPWM(1, 'CCW', 3000)
    # m.runASpecificWheelByPWM(2, 'CCW', 3000)
    # m.runASpecificWheelByPWM(3, 'CCW', 3000)
    # m.runASpecificWheelByPWM(4, 'CCW', 3000)
    # time.sleep(1)


    m.stopAllMotors()
