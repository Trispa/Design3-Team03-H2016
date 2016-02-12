from State import SendingBotToChargingStationState


class Sequencer :
    def setState(self, newState) :
        self.state = newState

    def __init__(self) :
        self.setState(SendingBotToChargingStationState.SendingBotToChargingStationState())

    def handleCurrentState(self):
        return self.state.handle(self)


