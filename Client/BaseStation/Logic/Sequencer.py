import SequencerState

class Sequencer :
    def setState(self, newState, robotPosition) :
        self.state = newState
        self.state.setPath(self.pathfinder, robotPosition)

    def __init__(self, pathfinder, robotPosition) :
        self.pathfinder = pathfinder
        self.setState(SequencerState.SendingBotToChargingStationState(), robotPosition)

    def handleCurrentState(self, obstacleListIndex, robotPosition):
        return self.state.handle(self, obstacleListIndex, robotPosition)


