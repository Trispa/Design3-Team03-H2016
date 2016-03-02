from State import SendingBotToChargingStationState


class Sequencer :
    def setState(self, newState) :
        self.state = newState
        self.state.initializePath()

    def visionCallToGetObstacleList(self):
        return "whatever"

    def __init__(self) :
        self.obstacleList = self.visionCallToGetObstacleList()
        self.setState(SendingBotToChargingStationState.SendingBotToChargingStationState())


    def handleCurrentState(self, obstacleListIndex):
        return self.state.handle(self, obstacleListIndex)


