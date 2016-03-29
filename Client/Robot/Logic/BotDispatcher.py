from ReferentialConverter import ReferentialConverter
from Client.Robot.VisionEmbarque.VisionRobot import VisionRobot
from Client.Robot.Mechanical.CameraTower import CameraTower
from Client.Robot.Mechanical.SerialPortCommunicator import SerialPortCommunicator
from Client.Robot.Mechanical.ManchesterCode import ManchesterCode
from Client.Robot.VisionEmbarque.tresorsDetection import TreasuresDetector

class BotDispatcher():
    def __init__(self, wheelManager):
        self.wheelManager = wheelManager
        self.vision = VisionRobot(wheelManager, CameraTower())

    def followPath(self, coordinates):
        print(coordinates)
        print("Bot going to "
      " : (" + str( coordinates["positionTOx"])+
      " " + str( coordinates["positionTOy"]) +
      ")")

        botPosition= (int(coordinates["positionFROMx"]),int(coordinates["positionFROMy"]))
        orientation = int(coordinates["orientation"])
        referentialConverter = ReferentialConverter(botPosition,orientation)
        pointConverted = referentialConverter.convertWorldToRobot((int(coordinates["positionTOx"]), int(coordinates["positionTOy"])))
        self.wheelManager.moveTo(pointConverted)

    def alignToTreasure(self):
        self.vision.approcheVersTresor()

    def detectTreasure(self):
        treasureDetector = TreasuresDetector()
        return treasureDetector.buildTresorsAngleList()

    def readManchester(self):
        serial = SerialPortCommunicator()
        manchester = ManchesterCode(serial)
        return manchester.getAsciiManchester()

