from Base.Logic.State import SendingBotToChargingStationState


class Sequencer :
    def setState(self, newState) :
        self.myState = newState

    def __init__(self) :
        self.setState(SendingBotToChargingStationState.SendingBotToChargingStationState())

    def handleCurrentState(self):
        self.myState.handle(self)


