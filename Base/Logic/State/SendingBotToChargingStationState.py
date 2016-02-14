import SendingBotToTreasureState

class SendingBotToChargingStationState():
    def handle(self, context):
        #call to pathfinder to return path to charging station
        context.setState(SendingBotToTreasureState.SendingBotToTreasureState())
