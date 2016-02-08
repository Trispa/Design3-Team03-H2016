import SendingBotToTreasureState

class AwaitingTargetState():
    def getNextState(self, context):
        context.setState(SendingBotToTreasureState.SendingBotToTreasureState())

    def handle(self):
        pass