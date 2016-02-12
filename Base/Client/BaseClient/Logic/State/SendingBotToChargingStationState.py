import json
import SendingBotToTreasureState

class SendingBotToChargingStationState():
    def handle(self, sequencer):
        sequencer.setState(SendingBotToTreasureState.SendingBotToTreasureState())
        #call to pathfinder to return path to charging station
        coordinates = {"type":"charging station",
                        "position": {
                            "positionX" : "12",
                            "positionY" : "50"
        }}
        return(coordinates)
