import SendingBotToChargingStationState

class AwaitingStartState():
    def getNextState(self, context):
        context.setState(SendingBotToChargingStationState.SendingBotToChargingStationState())

    def handle(self):
        pass