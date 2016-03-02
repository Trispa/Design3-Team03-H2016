import SendingBotToChargingStationState

class SendingBotToTargetState():

    def pathfinderCallMockup(self):
        return [(400,200), (500,200), (600,200), (700,150)]

    def __init__(self):
        self.obstacleIndex = 0
        self.path = self.pathfinderCallMockup()

    def handle(self, sequencer, obstacleListIndex):
        self.obstacleIndex = int(obstacleListIndex)
        print("sending bot to (" + str(self.path[int(obstacleListIndex)][0]) + "," +
              str(self.path[int(obstacleListIndex)][1]) + ")")

        coordinates = {"type": "target",
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
            sequencer.setState(SendingBotToChargingStationState.SendingBotToChargingStationState())
            coordinates["index"] = "-1"
            coordinates["end"] = "yes"

        return (coordinates)

