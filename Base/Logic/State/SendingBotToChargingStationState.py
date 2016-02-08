import AwaitingTargetState

class SendingBotToChargingStationState():
    def getNextState(self, context):
        context.setState(AwaitingTargetState.AwaitingTargetState())

    def handle(self):
        pass
