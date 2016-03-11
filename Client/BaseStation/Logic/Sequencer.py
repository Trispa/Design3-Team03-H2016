import SequencerState

class Sequencer :
    def setState(self, newState) :
        self.state = newState
        self.state.setPath(self.pathfinder)

    def __init__(self, pathfinder) :
        self.pathfinder = pathfinder
        self.setState(SequencerState.SendingBotToChargingStationState())

    def handleCurrentState(self, obstacleListIndex):
        value = self.state.handle(self, obstacleListIndex)
        print value
        return value


