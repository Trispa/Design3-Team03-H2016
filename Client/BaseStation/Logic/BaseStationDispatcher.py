from Client.BaseStation.WorldVision.worldVision import worldVision
from Client.BaseStation.Logic.Sequencer import Sequencer as seq
from Client.BaseStation.Logic.Pathfinding.Pathfinder import Pathfinder
from SequencerState import *
import cv2
import base64

class BaseStationDispatcher():
    def __init__(self):
        self.world = worldVision()

    def handleCurrentSequencerState(self, obstacleListIndex):
        map = self.world.getCurrentMap()
        return self.sequencer.handleCurrentState(obstacleListIndex, map.robot.square.findCenterOfMass(), map.robot.orientation)

    def initialiseWorldData(self):
        map = self.world.getCurrentMap()
        self.pathfinder = Pathfinder(map)
        self.sequencer = seq(self.pathfinder, map.robot.square.findCenterOfMass())
        return map.robot.square.findCenterOfMass(), map.robot.orientation

    def getCurrentWorldImage(self):
        image = self.world.getCurrentImage()
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
