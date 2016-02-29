import SendingBotToTreasureState


class SendingBotToChargingStationState():
    def handle(self, sequencer):
        #sequencer.setState(SendingBotToTreasureState.SendingBotToTreasureState())
        # call to pathfinder to return path to charging station
        coordinates = {"type": "charging station",
                       "positionTO": {
                           "positionX": "0",
                           "positionY": "100"},
                       "positionFROM": {
                           "positionX": "0",
                           "positionY": "0",
                           "orientation": "90"},
                       }
        return (coordinates)
