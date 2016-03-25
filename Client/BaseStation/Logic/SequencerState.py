class SendingBotToChargingStationState():
    def handle(self, sequencer, robotPosition, pathfinder):
        chargingStationPosition = (250,350)
        sequencer.setState(SendingBotToTreasureState())
        return pathfinder.findPath(robotPosition, chargingStationPosition)


class SendingBotToTreasureState():
    def handle(self, sequencer, robotPosition, pathfinder):
        sequencer.setState(SendingBotToTargetState())
        return  pathfinder.findPath(robotPosition, (2,5))


class SendingBotToTargetState():
    def handle(self, sequencer, robotPosition, pathfinder):
        sequencer.setState(SendingBotToChargingStationState())
        return pathfinder.findPath(robotPosition, (700,150))

