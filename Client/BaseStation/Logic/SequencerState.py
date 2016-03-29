from MapCoordinatesAjuster import MapCoordinatesAjuster

class SendingBotToChargingStationState():

    def handle(self, sequencer, map, pathfinder):
        mapCoordinatesAdjuster = MapCoordinatesAjuster(map)
        convertedPoint = mapCoordinatesAdjuster.convertPoint(map.robot.center)
        sequencer.setState(SendingBotToTreasureState())
        return pathfinder.findPath(convertedPoint, (905,55)), "alignPositionToChargingStation"

class SendingBotToTreasureState():
    def handle(self, sequencer, map, pathfinder):
        mapCoordinatesAdjuster = MapCoordinatesAjuster(map)
        convertedPoint = mapCoordinatesAdjuster.convertPoint(map.robot.center)
        sequencer.setState(SendingBotToTargetState())
        return  pathfinder.findPath(convertedPoint, (100,100)), "alignPositionToTreasure"


class SendingBotToTargetState():
    def handle(self, sequencer, map, pathfinder):
        mapCoordinatesAdjuster = MapCoordinatesAjuster(map)
        convertedTargetPosition = mapCoordinatesAdjuster.convertPoint(map.target.findCenterOfMass())
        convertedRobotPosition = mapCoordinatesAdjuster.convertPoint(map.robot.center)
        sequencer.setState(SendingBotToChargingStationState())
        return pathfinder.findPath(convertedRobotPosition, convertedTargetPosition), "alignPositionToTarget"

