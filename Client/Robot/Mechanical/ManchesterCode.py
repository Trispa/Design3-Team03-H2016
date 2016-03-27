import serial
import binascii
import re
import SerialPortCommunicator
from time import sleep
from collections import Counter

class ManchesterCode():

    READ_CODE_MANCHESTER = 4
    GET_CODE_MANCHESTER = 6
    ONE_SECOND_DELAY = 1
    ascii = []
    error = 0
    FALSE = 0
    TRUE = 1
    BIT_STOP_ERROR = "Bit stop errorne"
    CHAINE_VIDE_ERROR= "Chaine vide"
    def __init__(self, spc):
        self.spc = spc



######################manchester##################

    def readManchesterCode(self):
        self.spc._sendCommand(self.READ_CODE_MANCHESTER,self.FALSE,self.ONE_SECOND_DELAY, 1)


    def getManchesterCode(self):
       return  self.spc._sendCommand(self.GET_CODE_MANCHESTER,self.TRUE, self.ONE_SECOND_DELAY, 1)

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
            return (chaine_paire, chaine_paire.find(patern))    # c'Est mieu de retourner le l'index et la chaine avec str.index
        else:
            if(chaine_impaire.find(patern) != -1):

                return (chaine_impaire,chaine_impaire.find(patern)) #c'Est mieu de retourner le l'index et la chaine avec str.index

            else:
                return (-2, -1)


    def getCodebits(self):
        self.readManchesterCode()
        sleep(0.1)
        bits = self.getManchesterCode()
        if(bits ==""):
            return -1

        (chaine, indexPatern) = self.manchester_decode(bits)
        print(" chaine :", chaine)
        print("indexpaterne: ", indexPatern)
        if(chaine == -2):
            return -2
        data =  chaine[indexPatern + 9 : indexPatern + 16]
        #if(indexPatern > 7):
            #data =  chaine[indexPatern - 7 : indexPatern]
        #else:
            #data =  chaine[indexPatern + 9 : indexPatern + 16]

        print data[:: -1]
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

        while(nbr < 10  and self.error != -2 and self.error != -1):
            data = self.getCodebits()
            if(data == -2):
                self.error = -2
            elif(data == -1):
                self.error = -1
            else:
                lettre  = self.letter_from_bits(data)
                print lettre,
                self.ascii.append(lettre)
            nbr = nbr+1
        return (self.error)

    def getAsciiManchester(self):

        error = self.foundCodesManchester()
        if(self.error == 0 or self.ascii !=[]):
            word_counts = Counter(self.ascii)
            top_tree = word_counts.most_common(1)
            b = [str(i[0]) for i in top_tree]
            #print top_tree
            return  b[0]
        elif(self.error == -1):
            return self.CHAINE_VIDE_ERROR
        else:
            return self.BIT_STOP_ERROR

### Utilisation du code Manchester########

if __name__ == "__main__":
    spc = SerialPortCommunicator.SerialPortCommunicator()
    man = ManchesterCode(spc)
    letter = man.getAsciiManchester()

    print "ascii Code : ",letter