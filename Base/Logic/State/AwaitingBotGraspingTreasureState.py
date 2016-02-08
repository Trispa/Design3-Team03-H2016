import SendingBotToTargetState

class AwaitingBotGraspingTreasureState():
    def getNextState(self, context):
        context.setState(SendingBotToTargetState.SendingBotToTargetState())

    def handle(self):
        pass