class SendingBotToChargingStationState():
    def __init__(self):
        self.obstacleIndex = 0

    def setPath(self, pathfinder, robotPosition):
        self.path = pathfinder.findPath(robotPosition, (250,350))

    def handle(self, sequencer, obstacleListIndex, robotPosition, robotOrientation):
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
                           "positionX": robotPosition[0],
                           "positionY": robotPosition[1],
                           "orientation": robotOrientation},
                       }

        if(self.obstacleIndex == self.path.__len__() - 1):
            sequencer.setState(SendingBotToTreasureState(), (self.path[int(obstacleListIndex)][0],self.path[int(obstacleListIndex)][1]))
            coordinates["index"] = "-1"

        return (coordinates)

class SendingBotToTreasureState():
    def __init__(self):
        self.obstacleIndex = 0

    def setPath(self, pathfinder, robotPosition):
        self.path = pathfinder.findPath(robotPosition, (2,5))

    def handle(self, sequencer, obstacleListIndex, robotPosition, robotOrientation):
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
                           "positionX": robotPosition[0],
                           "positionY": robotPosition[1],
                           "orientation": robotOrientation},
                       }

        if(self.obstacleIndex == self.path.__len__() - 1):
            sequencer.setState(SendingBotToTargetState(), (self.path[int(obstacleListIndex)][0],self.path[int(obstacleListIndex)][1]))
            coordinates["index"] = "-1"

        return (coordinates)


class SendingBotToTargetState():
    def __init__(self):
        self.obstacleIndex = 0

    def setPath(self, pathfinder, robotPosition):
        self.path = pathfinder.findPath(robotPosition, (700,150))

    def handle(self, sequencer, obstacleListIndex, robotPosition, robotOrientation):
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
                           "positionX": robotPosition[0],
                           "positionY": robotPosition[1],
                           "orientation": robotOrientation},
                       }

        if(self.obstacleIndex == self.path.__len__() - 1):
            sequencer.setState(SendingBotToChargingStationState(), (self.path[int(obstacleListIndex)][0],self.path[int(obstacleListIndex)][1]))
            coordinates["index"] = "-1"
            coordinates["end"] = "yes"

        return (coordinates)

class SendingBotToChargingStationStateOnly():
    def __init__(self):
        self.obstacleIndex = 0

    def setPath(self, pathfinder, robotPosition):
        self.path = pathfinder.findPath(robotPosition, (250,350))

    def handle(self, sequencer, obstacleListIndex, robotPosition, robotOrientation):
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
                           "positionX": robotPosition[0],
                           "positionY": robotPosition[1],
                           "orientation": robotOrientation},
                       }

        if(self.obstacleIndex == self.path.__len__() - 1):
            sequencer.setState(SendingBotToChargingStationState(), (self.path[int(obstacleListIndex)][0],self.path[int(obstacleListIndex)][1]))
            coordinates["index"] = "-1"
            coordinates["end"] = "yes"

        return (coordinates)

class SendingBotToTreasureStateOnly():
    def __init__(self):
        self.obstacleIndex = 0

    def setPath(self, pathfinder, robotPosition):
        self.path = pathfinder.findPath(robotPosition, (2,5))

    def handle(self, sequencer, obstacleListIndex, robotPosition, robotOrientation):
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
                           "positionX": robotPosition[0],
                           "positionY": robotPosition[1],
                           "orientation": robotOrientation},
                       }

        if(self.obstacleIndex == self.path.__len__() - 1):
            sequencer.setState(SendingBotToChargingStationState(), (self.path[int(obstacleListIndex)][0],self.path[int(obstacleListIndex)][1]))
            coordinates["index"] = "-1"
            coordinates["end"] = "yes"

        return (coordinates)
