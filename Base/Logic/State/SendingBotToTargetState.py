import AwaitingStartState

class SendingBotToTargetState():
    def getNextState(self, context):
        context.setState(AwaitingStartState.AwaitingStartState())

    def handle(self):
        pass