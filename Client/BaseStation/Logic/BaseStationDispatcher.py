from Client.BaseStation.WorldVision.worldVision import worldVision
from Client.BaseStation.Logic.Sequencer import Sequencer as seq
from Client.BaseStation.Logic.Pathfinding.Pathfinder import Pathfinder
from TargetFactory import TargetFactory
from MapCoordinatesAjuster import MapCoordinatesAjuster
from SequencerState import *
import cv2
import base64

class BaseStationDispatcher():
    def __init__(self):
        self.world = worldVision()
        self.pathfinder = None
        self.path = None

    def handleCurrentSequencerState(self):
        image, map = self.world.getCurrentImage()
        self.path, signal = self.sequencer.handleCurrentState(map)
        return self.path, signal

    def initialiseWorldData(self):
        self.world.initializeRound()
        image, map = self.world.getCurrentImage()
        self.pathfinder = Pathfinder(map)
        mapCoordinatesAdjuster = MapCoordinatesAjuster(map)
        convertedPoint = mapCoordinatesAdjuster.convertPoint(map.robot.center)
        self.sequencer = seq(self.pathfinder, convertedPoint)
        return map.robot.center, map.robot.orientation

    def getCurrentWorldInformation(self):
        image, map = self.world.getCurrentImage()
        if(self.pathfinder != None):
            self.pathfinder.drawPath(image)
        convertedImage = cv2.imencode('.png',image)[1]
        base64ConvertedImage = base64.encodestring(convertedImage)
        mapCoordinatesAdjuster = MapCoordinatesAjuster(map)
        convertedPoint = mapCoordinatesAdjuster.convertPoint(map.robot.center)
        informationToSend = {"robotPosition":convertedPoint,
                           "robotOrientation":map.robot.orientation,
                           "encodedImage":base64ConvertedImage}
        return informationToSend

    def setTarget(self, jsonTarget):
        targetFactory = TargetFactory()
        target = targetFactory.constructTarget(jsonTarget)
        self.world.setTarget(target)
