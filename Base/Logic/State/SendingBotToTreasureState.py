import SendingBotToTargetState

class SendingBotToTreasureState():
    def handle(self, context):
        #call to pathfinder to return path to treasure
        context.setState(SendingBotToTargetState.SendingBotToTargetState())
