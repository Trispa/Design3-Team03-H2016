import SendingBotToTargetState


class SendingBotToTreasureState():
    def handle(self, sequencer):
        sequencer.setState(SendingBotToTargetState.SendingBotToTargetState())
        # call to pathfinder to return path to treasure
        coordinates = {"type": "treasure",
                       "position": {
                           "positionX": "500",
                           "positionY": "400"},
                       "positionFROM": {
                           "positionX": "0",
                           "positionY": "0",
                           "orientation": "0"},
                       }
        return (coordinates)
