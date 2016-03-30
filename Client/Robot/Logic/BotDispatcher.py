from ReferentialConverter import ReferentialConverter
from Client.Robot.VisionEmbarque.VisionRobot import VisionRobot
from Client.Robot.Mechanical.CameraTower import CameraTower
from Client.Robot.Mechanical.SerialPortCommunicator import SerialPortCommunicator
from Client.Robot.Mechanical.ManchesterCode import ManchesterCode
from Client.Robot.VisionEmbarque.tresorsDetection import TreasuresDetector
import platform
import cv2
from os import system



class BotDispatcher():
    def __init__(self, wheelManager):
        self.wheelManager = wheelManager
        self.cameraTower = CameraTower()

        if platform.linux_distribution()[0].lower() == "Ubuntu".lower():
            self.video = cv2.VideoCapture(1)
            system("v4l2-ctl --device=1 --set-ctrl gain=50")
        elif platform.linux_distribution()[0].lower() == "Fedora".lower():
            self.video = cv2.VideoCapture(0)
            system("v4l2-ctl --device=0 --set-ctrl gain=50")

        self.vision = VisionRobot(wheelManager,self.cameraTower, self.video )

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
        self.wheelManager.moveTo(pointConverted, referentialConverter)

    def alignToTreasure(self):
        self.vision.approcheVersTresor()

    def detectTreasure(self):
        treasureDetector = TreasuresDetector(self.cameraTower, self.video )
        return treasureDetector.buildTresorsAngleList()

    def readManchester(self):
        serial = SerialPortCommunicator()
        manchester = ManchesterCode(serial)
        return manchester.getAsciiManchester()

