from Client.BaseStation.Logic import SequencerState


class Sequencer :
    def setState(self, newState) :
        self.state = newState

    def __init__(self) :
        self.setState(SequencerState.SendingBotToChargingStationState())


    def handleCurrentState(self, obstacleListIndex):
        return self.state.handle(self, obstacleListIndex)


