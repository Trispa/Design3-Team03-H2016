from nanpy import ArduinoApi, SerialManager, Servo

class Arduino:
    def __init__(self):
        connection = SerialManager(device='/dev/ttyUSB0')
        self.a = ArduinoApi(connection=connection)

    def initCameraTower(self):
        pass