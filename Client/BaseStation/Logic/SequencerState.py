class SendingBotToChargingStationState():
    def __init__(self):
        self.obstacleIndex = 0

    def setPath(self, pathfinder, robotPosition):
        self.path = pathfinder.findPath(robotPosition, (250,350))

    def handle(self, sequencer, nodeListIndex, robotPosition, robotOrientation):
        self.obstacleIndex = int(nodeListIndex)

        print("sending bot to (" + str(self.path[int(nodeListIndex)].positionX) + "," +
              str(self.path[int(nodeListIndex)].positionY) + ")")

        coordinates = {"type": "charging station",
                       "endOfPhase":"no",
                       "endOfCycle":"no",
                       "index": str(self.obstacleIndex),
                       "positionTO": {
                           "positionX": str(self.path[int(nodeListIndex)].positionX),
                           "positionY": str(self.path[int(nodeListIndex)].positionY)},
                       "positionFROM": {
                           "positionX": robotPosition[0],
                           "positionY": robotPosition[1],
                           "orientation": robotOrientation},
                       }

        if(self.obstacleIndex == self.path.__len__() - 1):
            sequencer.setState(SendingBotToTreasureState(), (self.path[int(nodeListIndex)].positionX,self.path[int(nodeListIndex)].positionY))
            coordinates["index"] = "-1"
            coordinates["endOfPhase"] = "yes"

        return (coordinates)

class SendingBotToTreasureState():
    def __init__(self):
        self.obstacleIndex = 0

    def setPath(self, pathfinder, robotPosition):
        self.path = pathfinder.findPath(robotPosition, (2,5))

    def handle(self, sequencer, nodeListIndex, robotPosition, robotOrientation):
        self.obstacleIndex = int(nodeListIndex)

        print("sending bot to (" + str(self.path[int(nodeListIndex)].positionX) + "," +
              str(self.path[int(nodeListIndex)].positionY) + ")")

        coordinates = {"type": "treasure",
                       "endOfPhase":"no",
                       "endOfCycle":"no",
                       "index": str(self.obstacleIndex),
                       "positionTO": {
                           "positionX": str(self.path[int(nodeListIndex)].positionX),
                           "positionY": str(self.path[int(nodeListIndex)].positionY)},
                       "positionFROM": {
                           "positionX": robotPosition[0],
                           "positionY": robotPosition[1],
                           "orientation": robotOrientation},
                       }

        if(self.obstacleIndex == self.path.__len__() - 1):
            sequencer.setState(SendingBotToTargetState(), (self.path[int(nodeListIndex)].positionX,self.path[int(nodeListIndex)].positionY))
            coordinates["index"] = "-1"
            coordinates["endOfPhase"] = "yes"

        return (coordinates)


class SendingBotToTargetState():
    def __init__(self):
        self.obstacleIndex = 0

    def setPath(self, pathfinder, robotPosition):
        self.path = pathfinder.findPath(robotPosition, (700,150))

    def handle(self, sequencer, nodeListIndex, robotPosition, robotOrientation):
        self.obstacleIndex = int(nodeListIndex)
        print("sending bot to (" + str(self.path[int(nodeListIndex)].positionX) + "," +
              str(self.path[int(nodeListIndex)].positionY) + ")")

        coordinates = {"type": "target",
                       "endOfPhase":"no",
                       "endOfCycle":"no",
                       "index": str(self.obstacleIndex),
                       "positionTO": {
                           "positionX": str(self.path[int(nodeListIndex)].positionX),
                           "positionY": str(self.path[int(nodeListIndex)].positionY)},
                       "positionFROM": {
                           "positionX": robotPosition[0],
                           "positionY": robotPosition[1],
                           "orientation": robotOrientation},
                       }

        if(self.obstacleIndex == self.path.__len__() - 1):
            sequencer.setState(SendingBotToChargingStationState(), (self.path[int(nodeListIndex)].positionX,self.path[int(nodeListIndex)].positionY))
            coordinates["index"] = "-1"
            coordinates["endOfPhase"] = "yes"
            coordinates["endOfCycle"] = "yes"

        return (coordinates)

class SendingBotToChargingStationStateOnly():
    def __init__(self):
        self.obstacleIndex = 0

    def setPath(self, pathfinder, robotPosition):
        self.path = pathfinder.findPath(robotPosition, (250,350))

    def handle(self, sequencer, nodeListIndex, robotPosition, robotOrientation):
        self.obstacleIndex = int(nodeListIndex)

        print("sending bot to (" + str(self.path[int(nodeListIndex)].positionX) + "," +
              str(self.path[int(nodeListIndex)].positionY) + ")")

        coordinates = {"type": "charging station",
                       "endOfPhase":"no",
                       "endOfCycle":"no",
                       "index": str(self.obstacleIndex),
                       "positionTO": {
                           "positionX": str(self.path[int(nodeListIndex)].positionX),
                           "positionY": str(self.path[int(nodeListIndex)].positionY)},
                       "positionFROM": {
                           "positionX": robotPosition[0],
                           "positionY": robotPosition[1],
                           "orientation": robotOrientation},
                       }

        if(self.obstacleIndex == self.path.__len__() - 1):
            sequencer.setState(SendingBotToChargingStationState(), (self.path[int(nodeListIndex)].positionX,self.path[int(nodeListIndex)].positionY))
            coordinates["index"] = "-1"
            coordinates["endOfPhase"] = "yes"
            coordinates["endOfCycle"] = "yes"

        return (coordinates)

class SendingBotToTreasureStateOnly():
    def __init__(self):
        self.obstacleIndex = 0

    def setPath(self, pathfinder, robotPosition):
        self.path = pathfinder.findPath(robotPosition, (2,5))

    def handle(self, sequencer, nodeListIndex, robotPosition, robotOrientation):
        self.obstacleIndex = int(nodeListIndex)

        print("sending bot to (" + str(self.path[int(nodeListIndex)].positionX) + "," +
              str(self.path[int(nodeListIndex)].positionY) + ")")

        coordinates = {"type": "treasure",
                       "endOfPhase":"no",
                       "endOfCycle":"no",
                       "index": str(self.obstacleIndex),
                       "positionTO": {
                           "positionX": str(self.path[int(nodeListIndex)].positionX),
                           "positionY": str(self.path[int(nodeListIndex)].positionY)},
                       "positionFROM": {
                           "positionX": robotPosition[0],
                           "positionY": robotPosition[1],
                           "orientation": robotOrientation},
                       }

        if(self.obstacleIndex == self.path.__len__() - 1):
            sequencer.setState(SendingBotToChargingStationState(), (self.path[int(nodeListIndex)].positionX,self.path[int(nodeListIndex)].positionY))
            coordinates["index"] = "-1"
            coordinates["endOfPhase"] = "yes"
            coordinates["endOfCycle"] = "yes"

        return (coordinates)
