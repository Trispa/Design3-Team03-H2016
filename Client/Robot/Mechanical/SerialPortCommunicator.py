import serial
import binascii
import re
from time import sleep
import struct
from collections import Counter
import MoteurRoue

class SerialPortCommunicator:
    COMMAND_INDICATOR = "C"
    FALSE = 0
    TRUE = 1
    ONE_SECOND_DELAY = 1
    ONE_MINUTE_DELAY = 60
    FIVE_SECOND_DELAY = 5
    READ_CODE_MANCHESTER = 4
    GET_CODE_MANCHESTER = 6
    LED_FUNCTION_ON = 1
    LED_FUNCTION_OFF = 2
    CHANGE_MOTEUR_SPEED = 3
    STOP_ALL_MOTEUR = 5
    CW = 0
    CCW = 1

    ascii = []


    # def __init__(self, bitrateArduino = 9600, arduinoPort = "/dev/ttyUSB0"):
    #     STOP_ALL_MOTEUR = 4
    #     CW = 0
    #     CCW = 1

#Pololu : /dev/serial/by-id/pci-Pololu_Corporation_Pololu_Micro_Maestro_6-Servo_Controller_00021864-if0
    def __init__(self, bitrateArduino = 115200, arduinoPort = "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A7007dag-if00-port0"):
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

######################manchester##################

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
            return chaine_paire
        else:
            if(chaine_impaire.find(patern) != -1):

                return chaine_impaire
            else:
                print ("le patern 111111110 est pas bien choisi")
        return -2


    def getCodebits(self):
        trouve = 0
        indice = 0
        self.readManchesterCode()
        sleep(1)
        bits = self.getManchesterCode()
        chaine = self.manchester_decode(bits)
        if(chaine == -2):
            return -2

        c = ''
        data = ""
        patern = "111111110"
        if(chaine != ""):
            index = chaine.index(patern)
            print("index", index)
            #if(index >= 7):
            #indexTemp = index - 7
            data =  chaine[index + 9 : index + 16]
            #else:
                #data =  chaine[index + 9 : index + 15]
            # while  (trouve == 0):
            #     indice  = indice + 1
            #     bitStop = chaine[indice: indice+16]
            #     if(bitStop[:9] == patern):
            #         trouve == 1
            #         data = bitStop[9:]
            #         break
        else:
            return -1
        #print("chaine recu : "+chaine)
        print("code  : " + data)
        return data[:: -1]


    def letter_from_bits(self,bits, encoding='utf-8', errors='surrogatepass'):
        n = int(bits, 2)
        return self.int2bytes(n).decode(encoding, errors)

    def int2bytes(self, i):
        hex_string = '%x' % i
        n = len(hex_string)
        return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

    def foundCodesManchester(self):
        nbr = 0
        while(nbr< 10 ):
            data = self.getCodebits()
            if(data == -2):

                print "erreur"
                return -2
            else:
                lettre  = self.letter_from_bits(data)
                self.ascii.append(lettre)
            nbr = nbr+1
        return self.ascii

    def getAsciiManchester(self):
        self.foundCodesManchester()
        word_counts = Counter(self.ascii)
        top_tree = word_counts.most_common(1)
        b = [str(i[0]) for i in top_tree]
        print top_tree
        return  b[0]

### Utilisation du code Manchester########

if __name__ == "__main__":
    spc = SerialPortCommunicator()

    print spc.getAsciiManchester()

    #chaine = spc.getAsciiManchester()
    #if( chaine == -2):
        #print("ERREUR !")
    #else:
         #print("ASCII :" + chaine)
