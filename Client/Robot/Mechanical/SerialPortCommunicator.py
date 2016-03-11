import serial
from time import sleep
import struct
import binascii
import re

class SerialPortCommunicator:
    COMMAND_INDICATOR = "C"
    FALSE = 0
    TRUE = 1
    ONE_SECOND_DELAY = 1
    ONE_MINUTE_DELAY = 60
    FIVE_SECOND_DELAY = 5

    LED_FUNCTION_ON = 1
    LED_FUNCTION_OFF = 2
    CHANGE_MOTEUR_SPEED = 3
    READ_CODE_MANCHESTER = 4
    STOP_ALL_MOTEUR = 5
    GET_CODE_MANCHESTER = 6
    CW = 0
    CCW = 1



    # def __init__(self, bitrateArduino = 9600, arduinoPort = "/dev/ttyUSB0"):
    #     STOP_ALL_MOTEUR = 4
    #     CW = 0
    #     CCW = 1

#Pololu : /dev/serial/by-id/pci-Pololu_Corporation_Pololu_Micro_Maestro_6-Servo_Controller_00021864-if0
    def __init__(self, bitrateArduino = 9600, arduinoPort = "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A7007dag-if00-port0"):
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
        self._sendCommand(self.CHANGE_MOTEUR_SPEED, self.FALSE, self.ONE_SECOND_DELAY, noMoteur, speed*100, direction)

    def stopAllMotor(self):
        self._sendCommand(self.STOP_ALL_MOTEUR, self.FALSE, self.ONE_SECOND_DELAY, 1)

    #################################### MANCHESTER ################################
    def readManchesterCode(self):
        self._sendCommand(self.READ_CODE_MANCHESTER,self.FALSE,self.ONE_SECOND_DELAY, 1)


    def getManchesterCode(self):
       return  self._sendCommand(self.GET_CODE_MANCHESTER,self.TRUE, self.ONE_SECOND_DELAY, 1)

    def manchester_decode(self, chaine):
        i = 0
        chaine_paire = ""
        chaine_impaire = ""
        patern = "111111110"
        for  indice  in range(0, len(chaine)):
            if((indice % 2) == 0):
                chaine_paire += chaine[indice]
            else :
                chaine_impaire += chaine[indice]

        if(chaine_paire.find(patern) != -1):
            #chaine_paire = chaine_paire.replace(patern, '')
            print("dans la chaine paire")
            return chaine_paire
        else:
            if(chaine_impaire.find(patern) != -1):
                #chaine_impaire = re.sub(patern,"", chaine_impaire)
                print("dans la chaine impaire")
                return chaine_impaire
        return -2


    def getCodebits(self):
        trouve = 0
        indice = 0
        self.readManchesterCode()
        sleep(1)
        bits = self.getManchesterCode()
        chaine = self.manchester_decode(bits)

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
            return self.letter_from_bits(data)
        return -2
    #################################### END MANCHESTER ################################

if __name__ == "__main__":
    spc = SerialPortCommunicator()
    #maChaine = spc.getManchesterCode()
    #print(maChaine)
    #print(spc.getCodebits())
    print("ASCII :" + spc.getAsciiManchester())
