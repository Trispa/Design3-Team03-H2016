from State import SequencerState


class Sequencer :
    def setState(self, newState) :
        self.state = newState

    def visionCallToGetObstacleList(self):
        return "whatever"

    def __init__(self) :
        self.obstacleList = self.visionCallToGetObstacleList()
        self.setState(SequencerState.SendingBotToChargingStationState())


    def handleCurrentState(self, obstacleListIndex):
        return self.state.handle(self, obstacleListIndex)


