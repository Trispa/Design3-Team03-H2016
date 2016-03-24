import SequencerState

class Sequencer :
    def setState(self, newState, botPosition) :
        self.state = newState
        self.state.setPath(self.pathfinder, botPosition)

    def __init__(self, pathfinder, botPosition) :
        self.pathfinder = pathfinder
        self.setState(SequencerState.SendingBotToChargingStationState(), botPosition)

    def handleCurrentState(self, nodeListIndex, robotPosition, robotOrientation):
        print "POSITION OF ROBOT THAT I AM AWARE OF RIGHT NOW ", robotPosition
        return self.state.handle(self, nodeListIndex, robotPosition, robotOrientation)