import SendingBotToChargingStationState

class SendingBotToTargetState():
    def handle(self, context):
        context.setState(SendingBotToChargingStationState.SendingBotToChargingStationState())
        #call to pathfinder to return path to target
        return((50,60))
