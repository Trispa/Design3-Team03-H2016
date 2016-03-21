from State import FollowingPathState
from State import RefusingOrderState
from ReferentialConverter import ReferentialConverter

class BotDispatcher():
    def setState(self, newState) :
        self.state = newState

    def __init__(self, robot, wheelManager):
        self.robot = robot
        self.wheelManager = wheelManager
        self.setState(FollowingPathState.FollowingPathState())

    def initializeRobot(self, positionX, positionY, orientation):
        self.robot.positionX = positionX
        self.robot.positionY = positionY
        self.robot.orientation = orientation

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

        coordinates["positionTO"]["positionX"] = pointConverted[0]
        coordinates["positionTO"]["positionY"] = pointConverted[1]

        self.state.handle(self, coordinates)

    def refuseOrders(self):
        self.setState(RefusingOrderState.RefusingOrderState())

    def acceptOrders(self):
        self.setState(FollowingPathState.FollowingPathState())