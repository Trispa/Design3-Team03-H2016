from nanpy import ArduinoApi, SerialManager, Servo, ReadManchester
import time
import ctypes
#class ManchesterDecoder permet de decoder le code manchester
chaine = '\0'
class ManchesterDecoder:
    def __init__(self, ):
        self.manchester_buffer = []


    def manchester_decode(self, manchester_buffer):
        """
        :param manchester_buffer:
        :return: Decode a manchester array to a single data byte.
        """

def main():
        connection = SerialManager(device="/dev/ttyUSB0")
        man =  ReadManchester(2,3, connection = connection)
        #man.enableInterrupt(True);

        while(1):
            chaine = man.getMaschesterBits()
            if(chaine != '\0'):
                print(chaine)
                #man.enableInterrupt(False)




if __name__ == '__main__':
    main()



