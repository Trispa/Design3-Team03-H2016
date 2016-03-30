from ReferentialConverter import ReferentialConverter
from Client.Robot.VisionEmbarque.VisionRobot import VisionRobot
from Client.Robot.Mechanical.CameraTower import CameraTower
from Client.Robot.Mechanical.SerialPortCommunicator import SerialPortCommunicator
from Client.Robot.Mechanical.ManchesterCode import ManchesterCode
from Client.Robot.VisionEmbarque.tresorsDetection import TreasuresDetector
from Client.Robot.Mechanical.maestro import Controller
from Client.Robot.Mechanical.PositionAdjuster import PositionAdjuster
import platform
import cv2
from os import system



class BotDispatcher():
    def __init__(self, wheelManager):
        self.wheelManager = wheelManager
        self.maestro =Controller()
        self.cameraTower = CameraTower(self.maestro)
        self.treasureAngle = 0

        if platform.linux_distribution()[0].lower() == "Ubuntu".lower():
            self.video = cv2.VideoCapture(1)
            system("v4l2-ctl --device=1 --set-ctrl gain=50")
        elif platform.linux_distribution()[0].lower() == "Fedora".lower():
            self.video = cv2.VideoCapture(0)
            system("v4l2-ctl --device=0 --set-ctrl gain=50")

        self.vision = VisionRobot(wheelManager,self.cameraTower, self.video )
        self.positionAdjuster = PositionAdjuster(self.wheelManager, self.vision, self.maestro)


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
        self.positionAdjuster = None
        self.maestro = None
        self.maestro = Controller()
        self.positionAdjuster = PositionAdjuster(self.wheelManager, self.vision, self.maestro)
        self.positionAdjuster.approcheDuTresor()

    def detectTreasure(self):
        treasureDetector = TreasuresDetector(self.cameraTower, self.video )
        return treasureDetector.buildTresorsAngleList()

    def setRobotOrientation(self, robotAngle, angleToRotate):
        self.wheelManager.setOrientation(robotAngle, angleToRotate)

    def alignToChargingStation(self):
        self.positionAdjuster.approcheStationDeCharge()

    def returnToMap(self):
        self.positionAdjuster.chargementTerminer()


    def readManchester(self):
        serial = SerialPortCommunicator()
        manchester = ManchesterCode(serial)
        return manchester.getAsciiManchester()


