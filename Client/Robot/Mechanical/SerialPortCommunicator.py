import serial
from time import sleep
import struct
import binascii
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
    CHANGE_SPEED_LINE = 6
    CHANGE_SPEED_ROTATION = 7

    CW = 0
    CCW = 1

    # def __init__(self, bitrateArduino = 9600, arduinoPort = "/dev/ttyUSB0"):
    #     STOP_ALL_MOTEUR = 4
    #     CW = 0
    #     CCW = 1


    #/dev/serial/by-id/pci-FTDI_FT232R_USB_UART_A7007dag-if00-port0

    #Pololu : /dev/serial/by-id/pci-Pololu_Corporation_Pololu_Micro_Maestro_6-Servo_Controller_00021864-if0

    #Mon Port
    #def __init__(self, bitrateArduino = 115200, arduinoPort = "/dev/ttyACM1"):

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

    def _sendCommand(self, functionName, waitForCallback = 0, timeoutDelay = 1, *functionArgs):
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
        self._sendCommand(self.LED_FUNCTION_ON, self.FALSE, self.ONE_SECOND_DELAY, 1)

    def turnOffEndingLED(self):
        self._sendCommand(self.LED_FUNCTION_OFF, self.FALSE, self.ONE_SECOND_DELAY, 1)

    def driveMoteur(self, noMoteur, speed, direction):
        self._sendCommand(self.CHANGE_SINGLE_MOTEUR_SPEED, self.FALSE, self.ONE_SECOND_DELAY, noMoteur, speed * 100, direction)

    def stopAllMotor(self):
        self._sendCommand(self.STOP_ALL_MOTEUR, self.FALSE, self.ONE_SECOND_DELAY, 1)

    def driveMoteurLine(self, axe, speed, positif):
        self._sendCommand(self.CHANGE_SPEED_LINE, self.FALSE, self.ONE_SECOND_DELAY, axe, speed * 100, positif)

    def driveMoteurRotation(self, speed, direction):
        self._sendCommand(self.CHANGE_SPEED_ROTATION, self.FALSE, self.ONE_SECOND_DELAY, speed * 100, direction)

if __name__ == "__main__":
    spc = SerialPortCommunicator()
