from State import FollowingPathState
from ReferentialConverter import ReferentialConverter

class BotDispatcher():
    def setState(self, newState) :
        self.state = newState

    def __init__(self, wheelManager):
        self.wheelManager = wheelManager
        self.setState(FollowingPathState.FollowingPathState())

    def handleCurrentState(self, coordinates):
        print(coordinates)
        print("Bot going to "
      " : (" + str( coordinates["positionTOx"])+
      " " + str( coordinates["positionTOy"]) +
      ")")

        botPosition= (int(coordinates["positionFROMx"]),int(coordinates["positionFROMy"]))
        orientation = int(coordinates["orientation"])
        referentialConverter = ReferentialConverter(botPosition,orientation)
        pointConverted = referentialConverter.convertWorldToRobot((int(coordinates["positionTOx"]), int(coordinates["positionTOy"])))

        self.state.handle(self, pointConverted)
