import SequencerState

class Sequencer :
    def setState(self, newState) :
        self.state = newState

    def __init__(self, pathfinder) :
        self.pathfinder = pathfinder
        self.setState(SequencerState.SendingBotToChargingStationState())

    def handleCurrentState(self, nodeListIndex, robotPosition, robotOrientation):
        self.state.setPath(self.pathfinder, robotPosition)
        return self.state.handle(self, nodeListIndex, robotPosition, robotOrientation)


