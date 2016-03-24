from Client.BaseStation.WorldVision.worldVision import worldVision
from Client.BaseStation.Logic.Sequencer import Sequencer as seq
from Client.BaseStation.Logic.Pathfinding.Pathfinder import Pathfinder
from MapCoordinatesAjuster import MapCoordinatesAjuster
from SequencerState import *
import cv2
import base64

class BaseStationDispatcher():
    def __init__(self):
        self.world = worldVision()
        self.pathfinder = None

    def handleCurrentSequencerState(self, nodeListIndex):
        map = self.world.getCurrentMap()
        mapCoordinatesAdjuster = MapCoordinatesAjuster(map)
        convertedPoint = mapCoordinatesAdjuster.convertPoint(map.robot.square.findCenterOfMass())
        return self.sequencer.handleCurrentState(nodeListIndex, convertedPoint , map.robot.orientation)

    def initialiseWorldData(self):
        map = self.world.getCurrentMap()
        self.pathfinder = Pathfinder(map)
        mapCoordinatesAdjuster = MapCoordinatesAjuster(map)
        convertedPoint = mapCoordinatesAdjuster.convertPoint(map.robot.square.findCenterOfMass())
        self.sequencer = seq(self.pathfinder, convertedPoint)
        return map.robot.square.findCenterOfMass(), map.robot.orientation

    def getCurrentWorldImage(self):
        image = self.world.getCurrentImage()
        if(self.pathfinder != None):
            self.pathfinder.drawPath(image)
        convertedImage = cv2.imencode('.png',image)[1]
        base64ConvertedImage = base64.encodestring(convertedImage)
        return base64ConvertedImage

    def sendToChargingStation(self):
        map = self.world.getCurrentMap()
        robotPosition = map.robot.square.findCenterOfMass()
        self.sequencer.setState(SendingBotToChargingStationStateOnly(), robotPosition)

    def sendToTreasure(self):
        map = self.world.getCurrentMap()
        robotPosition = map.robot.square.findCenterOfMass()
        self.sequencer.setState(SendingBotToTreasureStateOnly(), robotPosition)
