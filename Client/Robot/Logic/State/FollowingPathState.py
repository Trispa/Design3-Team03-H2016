from Client.Robot.Logic.PositionAdjuster import *

class FollowingPathState():
    def __init__(self):
        self.sendingSignal = "needNewCoordinates"

    def handle(self, orderReceiver, coordinates):
        orderReceiver.wheelManager.moveTo(coordinates)