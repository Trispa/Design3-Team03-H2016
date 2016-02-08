from Base.Logic.State import AwaitingStartState


class Sequencer :
    def setState(self, newState) :
        self.myState = newState

    def __init__(self) :
        self.setState(AwaitingStartState.AwaitingStartState())

    def handleCurrentState(self):
        self.myState.handle(self)

    def assignNextState(self):
        self.myState.getNextState(self)

