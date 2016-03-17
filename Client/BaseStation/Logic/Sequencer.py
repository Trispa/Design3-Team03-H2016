import SequencerState

class Sequencer :
    def setState(self, newState) :
        self.state = newState
        self.state.setPath(self.pathfinder)

    def __init__(self, pathfinder) :
        self.pathfinder = pathfinder
        self.setState(SequencerState.SendingBotToChargingStationState())

    def handleCurrentState(self, obstacleListIndex, robotPosition):
        return self.state.handle(self, obstacleListIndex, robotPosition)


