from State import ExecutingOrderState
from State import RefusingOrderState
from ReferentialConverter import ReferentialConverter

import RobotMock

class OrderReceiver():
    def setState(self, newState) :
        self.state = newState
        #self.referentialConverter = ReferentialConverter(positionRobot, orientation);
        #self.wheelManager = WheelManager()

    def __init__(self):
        self.robot = RobotMock.RobotMock()
        self.setState(ExecutingOrderState.ExecutingOrderState())

    def handleCurrentState(self, coordinates):
        print("Bot going to " + coordinates[0]["type"] +
      " at : (" + coordinates[0]["position"]["positionX"] +
      " " + coordinates[0]["position"]["positionY"] +
      ")")

        #pointConverted = self.referentialConverter.convertWorldToRobot((int(coordinates[0]["position"]["positionX"]), int(coordinates[0]["position"]["positionY"]))
        pointConverted = (int(coordinates[0]["position"]["positionX"]), int(coordinates[0]["position"]["positionY"]))
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

    def initializeBot(self):
        print("initializing bot")
        self.robot.botInfo['voltage'] = "N/A"
        self.robot.botInfo['decodedCharacter'] = "N/A"
        self.robot.botInfo['target'] = "N/A"