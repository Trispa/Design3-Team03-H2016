from State import ExecutingOrderState
from State import RefusingOrderState
from ReferentialConverter import ReferentialConverter

class OrderReceiver():
    def setState(self, newState) :
        self.state = newState

    def __init__(self, robot, wheelManager):
        self.robot = robot
        self.wheelManager = wheelManager
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

        if(coordinates["end"] == "yes"):
            self.setState(RefusingOrderState.RefusingOrderState())

    def refuseOrders(self):
        self.setState(RefusingOrderState.RefusingOrderState())

    def acceptOrders(self):
        self.setState(ExecutingOrderState.ExecutingOrderState())