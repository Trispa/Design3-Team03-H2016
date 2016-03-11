class SendingBotToChargingStationState():
    def __init__(self):
        self.obstacleIndex = 0

    def setPath(self, pathfinder):
        self.path = pathfinder.findPath((0,0), (250,350))

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
            sequencer.setState(SendingBotToTreasureState())
            coordinates["index"] = "-1"
        print(coordinates)
        return (coordinates)

class SendingBotToTreasureState():
    def __init__(self):
        self.obstacleIndex = 0

    def setPath(self, pathfinder):
        self.path = pathfinder.findPath((0,0), (2,5))

    def handle(self, sequencer, obstacleListIndex):
        self.obstacleIndex = int(obstacleListIndex)

        print("sending bot to (" + str(self.path[int(obstacleListIndex)][0]) + "," +
              str(self.path[int(obstacleListIndex)][1]) + ")")

        coordinates = {"type": "treasure",
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
            sequencer.setState(SendingBotToTargetState())
            coordinates["index"] = "-1"

        return (coordinates)


class SendingBotToTargetState():
    def __init__(self):
        self.obstacleIndex = 0

    def setPath(self, pathfinder):
        self.path = pathfinder.findPath((400,200), (700,150))

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
            sequencer.setState(SendingBotToChargingStationState())
            coordinates["index"] = "-1"
            coordinates["end"] = "yes"

        return (coordinates)