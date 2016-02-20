import serial
from time import sleep
import struct

class SerialPortCommunicator:
    COMMAND_INDICATOR = "C"
    FALSE = 0
    TRUE = 1
    ONE_SECOND_DELAY = 1
    ONE_MINUTE_DELAY = 60

    LED_FUNCTION_ON = 1
    LED_FUNCTION_OFF = 2
    CHANGE_MOTEUR_SPEED = 3
    CW = 0
    CCW = 1

    def __init__(self, bitrateArduino = 115200, arduinoPort = "/dev/ttyUSB0"):
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
            receivedCallback = -1

        return receivedCallback

    def _packIntegerAsLong(self, value):
		return struct.pack('i', value)



    def turnOnEndingLED(self):
        self._sendCommand(self.LED_FUNCTION_ON, self.FALSE, self.ONE_SECOND_DELAY, 1)

    def turnOffEndingLED(self):
        self._sendCommand(self.LED_FUNCTION_OFF, self.FALSE, self.ONE_SECOND_DELAY, 1)
    def driveMoteur(self, noMoteur, speed, direction): #!!! speed * 100 !!!
        self._sendCommand(self.CHANGE_MOTEUR_SPEED, self.FALSE, self.ONE_SECOND_DELAY, noMoteur, speed, direction)

if __name__ == "__main__":
	spc = SerialPortCommunicator()
	spc.turnOnEndingLED()
	spc.driveMoteur(1, 20, 0)
	sleep(4)
	spc.driveMoteur(1, 30, 1)
	sleep(4)
	spc.driveMoteur(1, 0, 0)
	spc.turnOffEndingLED()
	sleep(1)
