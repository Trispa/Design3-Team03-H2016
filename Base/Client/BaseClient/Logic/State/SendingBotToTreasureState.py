import SendingBotToTargetState

class SendingBotToTreasureState():
    def handle(self, sequencer):
        sequencer.setState(SendingBotToTargetState.SendingBotToTargetState())
        #call to pathfinder to return path to treasure
        coordinates = {"type" : "treasure",
                      "position" : {
                            "positionX" : "45",
                            "positionY" : "90"
        }}
        return(coordinates)
