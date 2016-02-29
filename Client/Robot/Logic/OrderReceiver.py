from State import ExecutingOrderState
from State import RefusingOrderState
from ReferentialConverter import ReferentialConverter
from WheelManager import WheelManager

import RobotMock

class OrderReceiver():
    def setState(self, newState) :
        self.state = newState

        self.wheelManager = WheelManager()

    def __init__(self):
        self.robot = RobotMock.RobotMock()
        self.setState(ExecutingOrderState.ExecutingOrderState())

    def handleCurrentState(self, coordinates):
        print(coordinates)
        print("Bot going to " + coordinates[0]["type"] +
      " at : (" + coordinates[0]["positionTO"]["positionX"] +
      " " + coordinates[0]["positionTO"]["positionY"] +
      ")")

        botPosition= (int(coordinates[0]["positionFROM"]["positionX"]),int(coordinates[0]["positionFROM"]["positionY"]))
        orientation = int(coordinates[0]["positionFROM"]["orientation"])
        referentialConverter = ReferentialConverter(botPosition,orientation)
        pointConverted = referentialConverter.convertWorldToRobot((int(coordinates[0]["positionTO"]["positionX"]), int(coordinates[0]["positionTO"]["positionY"])))
        #pointConverted = (int(coordinates[0]["position"]["positionX"]), int(coordinates[0]["position"]["positionY"]))
        self.state.handle(self, pointConverted)

        #TODO Trouver une facon de se debarrasser de ce if la
        if(coordinates[0]["type"] == "target"):
            self.setState(RefusingOrderState.RefusingOrderState())

    def getCurrentRobotInformation(self):
        self.robot.botInfo['position'] = "(" + str(self.robot.positionX) + "," + str(self.robot.positionY) + ")"
        self.robot.botInfo['orientation'] = str(self.robot.orientation)
        return self.robot.botInfo

    def refuseOrders(self):
        self.setState(RefusingOrderState.RefusingOrderState())

    def acceptOrders(self):
        self.setState(ExecutingOrderState.ExecutingOrderState())

    def initializeBot(self, position, orientation):
        print("initializing bot")

        self.robot.botInfo['voltage'] = "N/A"
        self.robot.botInfo['decodedCharacter'] = "N/A"
        self.robot.botInfo['target'] = "N/A"