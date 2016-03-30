from Client.BaseStation.WorldVision.worldVision import worldVision
from Client.BaseStation.Logic.Sequencer import Sequencer as seq
from Client.BaseStation.Logic.Pathfinding.Pathfinder import Pathfinder
from TargetFactory import TargetFactory
import threading
from threading import current_thread
from SequencerState import *
import cv2
import base64

class BaseStationDispatcher():
    def __init__(self):
        self.world = worldVision()
        self.pathfinder = None
        self.path = None
        self.timer = None

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
        cv2.resize(image, (320,240))
        convertedImage = cv2.imencode('.png',image)[1]
        base64ConvertedImage = base64.encodestring(convertedImage)
        mapCoordinatesAdjuster = MapCoordinatesAjuster(map)
        convertedPoint = mapCoordinatesAdjuster.convertPoint(map.robot.center)

        informationToSend = {"robotPosition":convertedPoint,
                           "robotOrientation":map.robot.orientation,
                           "encodedImage":base64ConvertedImage}
        return informationToSend

    def startFromBegining(self):
        self.sequencer.setState(SendingBotToChargingStationState())

    def startFromTarget(self):
        self.sequencer.setState(SendingBotToTargetState())

    def startFromTreasure(self):
        self.sequencer.setState(SendingBotToTreasureState())

    def getCurrentMap(self):
        map = self.world.getCurrentMap()
        mapCoordinatesAdjuster = MapCoordinatesAjuster(map)
        convertedPoint = mapCoordinatesAdjuster.convertPoint(map.robot.center)
        informationToSend = {"robotPosition":convertedPoint,
                           "robotOrientation":map.robot.orientation}
        return informationToSend

    def setTarget(self, jsonTarget):
        targetFactory = TargetFactory()
        target = targetFactory.constructTarget(jsonTarget)
        self.world.setTarget(target)

    def setTreasuresOnMap(self, data):
        self.world.setTreasures(data)

    def setTimer(self, function,seconds):
        if self.timer != None:
            self.timer.cancel()
        def func_wrapper():
            self.setTimer(function, seconds)
            function()
        self.timer = threading.Timer(seconds, func_wrapper)
        self.timer.start()
        return self.timer