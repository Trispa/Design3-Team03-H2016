import SendingBotToChargingStationState


class SendingBotToTargetState():
    def handle(self, sequencer):
        sequencer.setState(SendingBotToChargingStationState.SendingBotToChargingStationState())
        # call to pathfinder to return path to target
        coordinates = {"type": "target",
                       "positionTO": {
                           "positionX": "0",
                           "positionY": "0"},
                       "positionFROM": {
                           "positionX": "0",
                           "positionY": "0",
                           "orientation": "0"},
                       }
        return (coordinates)
