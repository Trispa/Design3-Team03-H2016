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
    FALSE = 0
    TRUE = 1

    def __init__(self):
         self.spc = SerialPortCommunicator.SerialPortCommunicator()


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
    man = ManchesterCode()
    print man.getAsciiManchester()