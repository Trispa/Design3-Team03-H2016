from ReferentialConverter import ReferentialConverter
from Client.Robot.LocalVision.RobotVision import RobotVision
from Client.Robot.Mechanical.CameraTower import CameraTower
from Client.Robot.Mechanical.SerialPortCommunicator import SerialPortCommunicator
from Client.Robot.Mechanical.ManchesterCode import ManchesterCode
from Client.Robot.LocalVision.TreasuresDetector import TreasuresDetector
from Client.Robot.Mechanical.PositionAdjuster import PositionAdjuster
import platform
import cv2
from os import system



class BotDispatcher():
    def __init__(self, wheelManager, maestro, spc):
        self.wheelManager = wheelManager
        self.maestro = maestro
        self.cameraTower = CameraTower(self.maestro)
        self.treasureAngle = 0
        self.spc = spc

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

    def alignToTreasure(self, maestro):
        self.__initializeVideoCapture()
        self.vision = RobotVision(self.wheelManager, self.cameraTower, self.video)
        self.maestro = maestro
        self.positionAdjuster = PositionAdjuster(self.wheelManager, self.vision, self.maestro, self.spc)
        self.positionAdjuster.getCloserToTreasure()
        self.video.release()

    def detectTreasure(self):
        self.__initializeVideoCapture()
	print "Video supposed to be initialize is open : ", self.video.isOpened()
        treasureDetector = TreasuresDetector(self.cameraTower, self.video )
	anglesList = treasureDetector.buildTresorsAngleList()
        self.video.release()
        return anglesList

    def setRobotOrientation(self, robotAngle, angleToGetRobotTo):
        self.wheelManager.setOrientation(robotAngle, angleToGetRobotTo)

    def alignToChargingStation(self):
        self.__initializeVideoCapture()
        self.vision = RobotVision(self.wheelManager, self.cameraTower, self.video)
        self.positionAdjuster = PositionAdjuster(self.wheelManager, self.vision, self.maestro, self.spc)
        self.positionAdjuster.getCloserToChargingStation()
        self.video.release()

    def getRobotBackOnMap(self):
        self.positionAdjuster.stopCharging()

    def readManchester(self):
        serial = SerialPortCommunicator()
        manchester = ManchesterCode(serial)
        return manchester.getAsciiManchester()

    def __initializeVideoCapture(self):
        if platform.linux_distribution()[0].lower() == "Ubuntu".lower():
            self.video = cv2.VideoCapture(1)
            system("v4l2-ctl --device=1 --set-ctrl gain=50")
        elif platform.linux_distribution()[0].lower() == "Fedora".lower():
            self.video = cv2.VideoCapture(0)
            system("v4l2-ctl --device=1 -c brightness=128 -c gain=129 -c exposure_auto=1")
            system("v4l2-ctl --device=1 -c exposure_absolute=275")
        # else:
        #     self.video = cv2.VideoCapture(0)
