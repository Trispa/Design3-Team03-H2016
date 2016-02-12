import SendingBotToTreasureState

class SendingBotToChargingStationState():
    def handle(self, context):
        context.setState(SendingBotToTreasureState.SendingBotToTreasureState())
        #call to pathfinder to return path to charging station
        return((12,50))
