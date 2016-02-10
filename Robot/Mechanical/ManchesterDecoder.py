from nanpy import ArduinoApi, SerialManager, Servo
import time

#class ManchesterDecoder permet de decoder le code manchester

class ManchesterDecoder:
    def __init__(self, ):
        self.manchester_buffer = []


    def manchester_decode(self, manchester_buffer):
        """
        :param manchester_buffer:
        :return: Decode a manchester array to a single data byte.
        """
        decoded = 0
        for i in range(0, 8):
            bit = 7 - i;
            # Use the second value of each encoded bit, as that is the bit value
            # eg. 1 is encoded to [0, 1], so retrieve the second bit (1)
            decoded |= manchester_buffer[4 + (i * 2) + 1] << (bit)
        return decoded

def main():
    connection = SerialManager(device='COM3')
    a = ArduinoApi(connection = connection)
    pinManchester = 3
    pinClock = 2
    a.pinMode(pinManchester, a.INPUT)
    a.pinMode(pinClock, a.INPUT)
    trame  = []

    while(1):

        bit = a.digitalRead(pinManchester)
        print(bit)
        trame.append(bit)

    decoder = ManchesterDecoder()
    decoder.manchester_buffer = trame
    decoded = decoder.manchester_decode(decoder.manchester_buffer)

    print(decoded)
if __name__ == '__main__':
    main()


