class SendingBotToChargingStationState():
    def handle(self, sequencer, robotPosition, pathfinder):
        chargingStationPosition = (100,100)
        sequencer.setState(SendingBotToTreasureState())
        bob = pathfinder.findPath(robotPosition, chargingStationPosition)
        return bob


class SendingBotToTreasureState():
    def handle(self, sequencer, robotPosition, pathfinder):
        sequencer.setState(SendingBotToTargetState())
        return  pathfinder.findPath(robotPosition, (2,5))


class SendingBotToTargetState():
    def handle(self, sequencer, robotPosition, pathfinder):
        sequencer.setState(SendingBotToChargingStationState())
        return pathfinder.findPath(robotPosition, (700,150))

