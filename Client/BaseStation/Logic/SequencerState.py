from MapCoordinatesAjuster import MapCoordinatesAjuster

class SendingBotToChargingStationState():
    def handle(self, sequencer, map, pathfinder):
        mapCoordinatesAdjuster = MapCoordinatesAjuster(map)
        convertedPoint = mapCoordinatesAdjuster.convertPoint(map.robot.center)
        sequencer.setState(DetectTreasureState())
        safeSpot = pathfinder.findGoodPoint((895,110))
        return pathfinder.findPath(convertedPoint, safeSpot), "rotateToChargingStation", 270


class DetectTreasureState():
    def handle(self, sequencer, map, pathfinder):
        mapCoordinatesAdjuster = MapCoordinatesAjuster(map)
        convertedPoint = mapCoordinatesAdjuster.convertPoint(map.robot.center)
        sequencer.setState(SendingBotToTreasureState())
        safeSpot = pathfinder.findGoodPoint((800,250))
        return  pathfinder.findPath(convertedPoint,safeSpot), "rotateToDetectTreasure", 180

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
        targetPosition, orientationToGo = map.getPositionInFrontOfIsland()
        convertedTargetPosition = mapCoordinatesAdjuster.convertPoint(targetPosition)
        convertedRobotPosition = mapCoordinatesAdjuster.convertPoint(map.robot.center)
        sequencer.setState(StopMovingState())
        return pathfinder.findPath(convertedRobotPosition, convertedTargetPosition), "alignPositionToTarget", orientationToGo

class StopMovingState():
    def handle(self, sequencer, map, pathfinder):
        return None, None, None

