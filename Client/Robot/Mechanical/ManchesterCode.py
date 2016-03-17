import binascii
import re
import SerialPortCommunicator
from time import sleep

class ManchesterCode(SerialPortCommunicator):

    READ_CODE_MANCHESTER = 4
    GET_CODE_MANCHESTER = 6
    ONE_SECOND_DELAY = 1

    def __init__(self):
        SerialPortCommunicator.__init__(self)


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
                #chaine_impaire = re.sub(patern,"", chaine_impaire)

                return chaine_impaire
        return -2


    def getCodebits(self):
        trouve = 0
        indice = 0
        self.readManchesterCode()
        sleep(2)
        bits = self.getManchesterCode()
        chaine = self.manchester_decode(bits)
        if(chaine == -2):
            return -2

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
        if(data == -2):
             return -2
        else:
            return self.letter_from_bits(data)



### Utilisation du code Manchester########

if __name__ == "__main__":
    man = ManchesterCode()
    chaine = man.getAsciiManchester()# le code ASCII est retourné dans le string chaine
    if( chaine == -2):
        print("ERREUR !")
    else:
         print("ASCII :" + chaine)