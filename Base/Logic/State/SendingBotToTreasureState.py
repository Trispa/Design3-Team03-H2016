import AwaitingBotGraspingTreasureState

class SendingBotToTreasureState():
    def getNextState(self, context):
        context.setState(AwaitingBotGraspingTreasureState.AwaitingBotGraspingTreasureState())

    def handle(self):
        pass