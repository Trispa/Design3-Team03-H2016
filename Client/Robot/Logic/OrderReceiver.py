from State import ExecutingOrderState
from State import RefusingOrderState
from ReferentialConverter import ReferentialConverter
from WheelManager import WheelManager

import RobotMock

class OrderReceiver():
    def setState(self, newState) :
        self.state = newState

    def __init__(self, robot):
        self.robot = robot
        #self.wheelManager = wheelManager
        self.setState(ExecutingOrderState.ExecutingOrderState())

    def handleCurrentState(self, coordinates):
        print(coordinates)
        print("Bot going to " + coordinates["type"] +
      " at : (" + coordinates["positionTO"]["positionX"] +
      " " + coordinates["positionTO"]["positionY"] +
      ")")

        botPosition= (int(coordinates["positionFROM"]["positionX"]),int(coordinates["positionFROM"]["positionY"]))
        orientation = int(coordinates["positionFROM"]["orientation"])
        referentialConverter = ReferentialConverter(botPosition,orientation)
        pointConverted = referentialConverter.convertWorldToRobot((int(coordinates["positionTO"]["positionX"]), int(coordinates["positionTO"]["positionY"])))
        #pointConverted = (int(coordinates[0]["position"]["positionX"]), int(coordinates[0]["position"]["positionY"]))
        self.state.handle(self, pointConverted)

        #TODO Trouver une facon de se debarrasser de ce if la
        if(coordinates["type"] == "target"):
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