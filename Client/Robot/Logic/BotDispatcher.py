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
        self.botVoltage = 0
        self.spc = spc
        self.serialPortCommunicatorIsReadByManchester = False
        self.lastPositionGoneTo = (0,0)

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
        self.serialPortCommunicatorIsReadByManchester = True
        self.wheelManager.moveTo(pointConverted)
        self.serialPortCommunicatorIsReadByManchester = False

    def alignToTreasure(self, maestro):
        self.__initializeVideoCapture()
        self.vision = RobotVision(self.wheelManager, self.cameraTower, self.video)
        self.maestro = maestro
        self.positionAdjuster = PositionAdjuster(self.wheelManager, self.vision, self.maestro, self.spc)
        self.serialPortCommunicatorIsReadByManchester = True
        self.positionAdjuster.getCloserToTreasure()
        self.serialPortCommunicatorIsReadByManchester = False
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
        self.serialPortCommunicatorIsReadByManchester = True
        self.positionAdjuster.getCloserToChargingStation()
        self.serialPortCommunicatorIsReadByManchester = False
        self.video.release()

    def getRobotBackOnMapAfterCharging(self):
        self.serialPortCommunicatorIsReadByManchester = True
        self.positionAdjuster.stopCharging()
        self.serialPortCommunicatorIsReadByManchester = False

    def getRobotBackOnMapWhenOutOfBound(self):
        self.serialPortCommunicatorIsReadByManchester = True
        self.positionAdjuster.getBackToMapAfterGrabingBackgroundTreausre()
        self.serialPortCommunicatorIsReadByManchester = False

    def readManchester(self):
        serial = SerialPortCommunicator()
        manchester = ManchesterCode(serial)
        return manchester.getAsciiManchester()

    def alignToTargetIsland(self):
        self.__initializeVideoCapture()
        self.vision = RobotVision(self.wheelManager, self.cameraTower, self.video)
        self.positionAdjuster = PositionAdjuster(self.wheelManager, self.vision, self.maestro, self.spc)
        self.serialPortCommunicatorIsReadByManchester = True
        self.positionAdjuster.getCloserToIsland()
        self.serialPortCommunicatorIsReadByManchester = False
        self.video.release()

    def alignToTargetIslandTest(self, color):
        self.__initializeVideoCapture()
        self.vision = RobotVision(self.wheelManager, self.cameraTower, self.video)
        self.positionAdjuster = PositionAdjuster(self.wheelManager, self.vision, self.maestro, self.spc)
        self.serialPortCommunicatorIsReadByManchester = True
        self.positionAdjuster.alignToIsland(color)
        self.serialPortCommunicatorIsReadByManchester = False
        self.video.release()

    def __initializeVideoCapture(self):
        if platform.linux_distribution()[0].lower() == "Ubuntu".lower():
            self.video = cv2.VideoCapture(1)
            system("v4l2-ctl --device=1 --set-ctrl gain=50")
        elif platform.linux_distribution()[0].lower() == "Fedora".lower():
            self.video = cv2.VideoCapture(0)

          #  system("echo 'Hello world4'")
            #system("v4l2-ctl -c white_balance_temperature=1500")

        # else:
        #     self.video = cv2.VideoCapture(0)
