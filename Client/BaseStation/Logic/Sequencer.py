import SequencerState

class Sequencer :
    def setState(self, newState) :
        self.state = newState

    def __init__(self, pathfinder, botPosition) :
        self.pathfinder = pathfinder
        self.setState(SequencerState.SendingBotToChargingStationState())

    def handleCurrentState(self, map):
        return self.state.handle(self, map, self.pathfinder)