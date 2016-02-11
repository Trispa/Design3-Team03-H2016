import SendingBotToTargetState

class SendingBotToTreasureState():
    def handle(self, context):
        context.setState(SendingBotToTargetState.SendingBotToTargetState())
        #call to pathfinder to return path to treasure
        return((45,90))
