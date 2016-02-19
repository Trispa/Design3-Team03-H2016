import SendingBotToChargingStationState

class SendingBotToTargetState():
    def handle(self, sequencer):
        sequencer.setState(SendingBotToChargingStationState.SendingBotToChargingStationState())
        #call to pathfinder to return path to target
        coordinates = {"type" : "target",
                        "position": {
                            "positionX" : "800",
                            "positionY" : "200"
        }}
        return(coordinates)

