import serial
from time import sleep
import struct
import platform

class SerialPortCommunicator:
    COMMAND_INDICATOR = "C"
    FALSE = 0
    TRUE = 1
    ONE_SECOND_DELAY = 1
    ONE_MINUTE_DELAY = 60

    LED_FUNCTION_ON = 1
    LED_FUNCTION_OFF = 2
    CHANGE_SINGLE_MOTEUR_SPEED = 3
    STOP_ALL_MOTEUR = 5
    CHANGE_SPEED_LINE = 7
    CHANGE_SPEED_ROTATION = 8
    CHANGE_CONDENSATOR_MODE = 9
    READ_VOLTAGE = 10

    CW = 0
    CCW = 1

    tensionCondensateur = 0



    # def __init__(self, bitrateArduino = 9600, arduinoPort = "/dev/ttyUSB0"):
    #     STOP_ALL_MOTEUR = 4
    #     CW = 0
    #     CCW = 1

#Pololu : /dev/serial/by-id/pci-Pololu_Corporation_Pololu_Micro_Maestro_6-Servo_Controller_00021864-if0

    #Ubuntu pci-FTDI...
    #Fedora usb-FTDI...

    def __init__(self, bitrateArduino = 115200, arduinoPort = "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A7007dag-if00-port0"):
        if platform.linux_distribution()[0].lower() == "Ubuntu".lower():
            arduinoPort = "/dev/serial/by-id/pci-FTDI_FT232R_USB_UART_A7007dag-if00-port0"
        elif platform.linux_distribution()[0].lower() == "Fedora".lower():
            arduinoPort = "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A7007dag-if00-port0"
        self.arduino = serial.Serial(arduinoPort, bitrateArduino, timeout = 1)
        #self.polulu = serial.Serial(poluluPort, bitratePolulu, timeout = 1)
        sleep(1)

    def sendCommand(self, functionName, waitForCallback = 0, timeoutDelay = 1, *functionArgs):
        command = self.COMMAND_INDICATOR + str(functionName) + str(waitForCallback) + str(len(functionArgs))
        self.arduino.write(command)

        for arguments in functionArgs:
            self.arduino.write(self._packIntegerAsLong(arguments))
        #self.arduino.write(str(arguments))

        if waitForCallback:
            return self._readCallback(timeoutDelay)

    def _readCallback(self, timeoutDelay):
        waitedTime = 0
        while self.arduino.read() != "R" and waitedTime < timeoutDelay:
            sleep(0.1)
            waitedTime += 0.1

        if waitedTime < timeoutDelay:
            receivedCallback = self.arduino.readline()
        else:
            # receivedCallback = -1
            receivedCallback = self.arduino.readline()

        return receivedCallback

    def _packIntegerAsLong(self, value):
        return struct.pack('i', value)



    def turnOnEndingLED(self):
        self.sendCommand(self.LED_FUNCTION_ON, self.FALSE, self.ONE_SECOND_DELAY, 1)

    def turnOffEndingLED(self):
        self.sendCommand(self.LED_FUNCTION_OFF, self.FALSE, self.ONE_SECOND_DELAY, 1)

    def driveMoteur(self, noMoteur, speed, direction):
        self.sendCommand(self.CHANGE_SINGLE_MOTEUR_SPEED, self.FALSE, self.ONE_SECOND_DELAY, noMoteur, speed * 100, direction)

    def stopAllMotor(self):
        self.sendCommand(self.STOP_ALL_MOTEUR, self.FALSE, self.ONE_SECOND_DELAY, 1)

    def driveMoteurLine(self, axe, speed, positif, distance):
        tmpVoltage = self.sendCommand(self.CHANGE_SPEED_LINE, self.TRUE, self.ONE_SECOND_DELAY, axe, speed * 100, positif, distance * 100)
        if tmpVoltage == '':
            self.tensionCondensateur = 0
        else:
            self.tensionCondensateur = float(tmpVoltage) / 100.0

    def driveMoteurRotation(self, speed, direction, angle):
        tmpVoltage = self.sendCommand(self.CHANGE_SPEED_ROTATION, self.TRUE, self.ONE_SECOND_DELAY, speed * 100, direction, angle * 100)
        if tmpVoltage == '':
            self.tensionCondensateur = 0
        else:
            self.tensionCondensateur = float(tmpVoltage) / 100.0

    #/controle electro aiment 00 decharge 10 ou 01 garde la charge 11 pour recharger
    # // 0 decharge magnetique
    # // 1 ou else garde charge
    # // 2 recharge
    def changeCondensatorMode(self, mode):
        self.sendCommand(self.CHANGE_CONDENSATOR_MODE, self.FALSE, self.ONE_SECOND_DELAY, mode)

    def readConsensatorVoltage(self):
        tmpTempo = self.sendCommand(self.LED_FUNCTION_ON, self.TRUE, self.ONE_SECOND_DELAY, 1)
        if tmpTempo == '':
            self.tensionCondensateur = 0
        else:
            self.tensionCondensateur = float(tmpTempo) / 100.0
        return self.tensionCondensateur

    def getTensionCondensateur(self):
        return self.tensionCondensateur



if __name__ == "__main__":
    spc = SerialPortCommunicator()
    spc.changeCondensatorMode(2)

    v = spc.readConsensatorVoltage()

    while v <= 3:
        sleep(1)
        v = spc.readConsensatorVoltage()
        print "Voltage : ", v

    spc.changeCondensatorMode(1)
    a = raw_input("Press enter to active magnet")
    spc.changeCondensatorMode(0)

    while True:
        sleep(1)
        v = spc.readConsensatorVoltage()
        print "Voltage : ", v


