import serial
from time import sleep
import struct
import binascii

class SerialPortCommunicator:
    COMMAND_INDICATOR = "C"
    FALSE = 0
    TRUE = 1
    ONE_SECOND_DELAY = 1
    ONE_MINUTE_DELAY = 60

    LED_FUNCTION_ON = 1
    LED_FUNCTION_OFF = 2
    CHANGE_MOTEUR_SPEED = 3
    GET_CODE_MANCHESTER = 4
    STOP_ALL_MOTEUR = 5
    CW = 0
    CCW = 1


    def __init__(self, bitrateArduino = 9600, arduinoPort = "/dev/ttyUSB0"):
        STOP_ALL_MOTEUR = 4
        CW = 0
        CCW = 1


    def __init__(self, bitrateArduino = 115200, arduinoPort = "/dev/ttyUSB1"):
        #self.arduino = serial.Serial(arduinoPort, bitrateArduino, timeout = 1)
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
        self._sendCommand(self.CHANGE_MOTEUR_SPEED, self.FALSE, self.ONE_SECOND_DELAY, noMoteur, speed*100, direction)

    def stopAllMotor(self):
        self._sendCommand(self.STOP_ALL_MOTEUR, self.FALSE, self.ONE_SECOND_DELAY, 1)

     #################################### MANCHESTER ################################
    def getManchesterCode(self):
        return self._sendCommand(self.GET_CODE_MANCHESTER,self.TRUE,self.ONE_SECOND_DELAY, 1)

    def getCodebits(self):
        trouve = 0
        indice = 0
        chaine = self.getManchesterCode();
        c = ''
        data = ""
        patern = "111111110"
        if(chaine != ""):
            while  (trouve == 0):
                indice  = indice + 1
                bitStop = chaine[indice: indice+16]
                if(bitStop[:9] == patern):
                    trouve == 1
                    data = bitStop[9:]
                    break
        else:
            return -1
        print("chaine recu : "+chaine)
        print("code  : " + data)
        return data

    def letter_from_bits(self,bits, encoding='utf-8', errors='surrogatepass'):
        n = int(bits, 2)
        return self.int2bytes(n).decode(encoding, errors)

    def int2bytes(self, i):
        hex_string = '%x' % i
        n = len(hex_string)
        return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

    def getAsciiManchester(self):
        data = self.getCodebits()
        if(data == -1):
            print ("la chaine recu est vide ")
        else:
            return spc.letter_from_bits(data)
        return -2
        #################################### END MANCHESTER ################################

if __name__ == "__main__":
    spc = SerialPortCommunicator()
    letter = spc.getAsciiManchester()
    if(letter ==-2):
        print("Erreur")
    else:
        print("ASCII :" + letter)
    spc.stopAllMotor()

    print(spc.getAsciiManchester())

