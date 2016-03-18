from Client.BaseStation.WorldVision.worldVision import worldVision
from Client.BaseStation.Logic.Sequencer import Sequencer as seq
from Client.BaseStation.Logic.Pathfinding.Pathfinder import Pathfinder
import cv2
import base64

class BaseStationDispatcher():
    def __init__(self):
        self.world = worldVision()

    def handleCurrentSequencerState(self, obstacleListIndex):
        map = self.world.getCurrentMap()
        return self.sequencer.handleCurrentState(obstacleListIndex, map.robot.findCenterOfMass())

    def initialiseWorldData(self):
        map = self.world.getCurrentMap()
        self.pathfinder = Pathfinder(map)
        self.sequencer = seq(self.pathfinder, map.robot.findCenterOfMass())

    def getCurrentWorldImage(self):
        image = self.world.getCurrentImage()
        convertedImage = cv2.imencode('.png',image)[1]
        base64ConvertedImage = base64.encodestring(convertedImage)
        return base64ConvertedImage
