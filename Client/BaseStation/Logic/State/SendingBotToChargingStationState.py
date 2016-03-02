import SendingBotToTreasureState


class SendingBotToChargingStationState():
    def pathfinderCallMockup(self):
        return [(0,0), (100,100), (150, 200), (200,200), (250,200), (250,300), (250,350)]

    def __init__(self):
        self.obstacleIndex = 0
        self.path = self.pathfinderCallMockup()

    def handle(self, sequencer, obstacleListIndex):
        self.obstacleIndex = int(obstacleListIndex)

        print("sending bot to (" + str(self.path[int(obstacleListIndex)][0]) + "," +
              str(self.path[int(obstacleListIndex)][1]) + ")")

        coordinates = {"type": "charging station",
                       "end":"no",
                       "index": str(self.obstacleIndex),
                       "positionTO": {
                           "positionX": str(self.path[int(obstacleListIndex)][0]),
                           "positionY": str(self.path[int(obstacleListIndex)][1])},
                       "positionFROM": {
                           "positionX": "0",
                           "positionY": "0",
                           "orientation": "0"},
                       }


        if(self.obstacleIndex == self.path.__len__() - 1):
            sequencer.setState(SendingBotToTreasureState.SendingBotToTreasureState())
            coordinates["index"] = "-1"

        return (coordinates)
