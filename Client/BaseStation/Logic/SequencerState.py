from MapCoordinatesAjuster import MapCoordinatesAjuster

class SendingBotToChargingStationState():
    def handle(self, sequencer, map, pathfinder):
        mapCoordinatesAdjuster = MapCoordinatesAjuster(map)
        convertedPoint = mapCoordinatesAdjuster.convertPoint(map.robot.center)
        sequencer.setState(DetectTreasureState())
        return pathfinder.findPath(convertedPoint, (885,100)), "rotateToChargingStation", 270


class DetectTreasureState():
    def handle(self, sequencer, map, pathfinder):
        mapCoordinatesAdjuster = MapCoordinatesAjuster(map)
        convertedPoint = mapCoordinatesAdjuster.convertPoint(map.robot.center)
        sequencer.setState(SendingBotToTreasureState())
        return  pathfinder.findPath(convertedPoint, (850,200)), "detectTreasure", 180

class SendingBotToTreasureState():
    def handle(self, sequencer, map, pathfinder):
        mapCoordinatesAdjuster = MapCoordinatesAjuster(map)
        treasurePosition, orientationToGo = map.getPositionInFrontOfTreasure()
        convertedRobotPosition = mapCoordinatesAdjuster.convertPoint(map.robot.center)
        convertedTreasurePosition = mapCoordinatesAdjuster.convertPoint(treasurePosition)
        sequencer.setState(SendingBotToTargetState())
        return  pathfinder.findPath(convertedRobotPosition, convertedTreasurePosition), "rotateToTreasure", orientationToGo


class SendingBotToTargetState():
    def handle(self, sequencer, map, pathfinder):
        mapCoordinatesAdjuster = MapCoordinatesAjuster(map)
        convertedTargetPosition = mapCoordinatesAdjuster.convertPoint(map.target.findCenterOfMass())
        convertedRobotPosition = mapCoordinatesAdjuster.convertPoint(map.robot.center)
        sequencer.setState(StopMovingState())
        return pathfinder.findPath(convertedRobotPosition, convertedTargetPosition), "alignPositionToTarget", 90

class StopMovingState():
    def handle(self, sequencer, map, pathfinder):
        return None, None, None

