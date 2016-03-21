from Client.Robot.Logic.PositionAdjuster import *
from RefusingOrderState import RefusingOrderState

class FollowingPathState():
    def __init__(self):
        self.sendingSignal = "needNewCoordinates"

    def handle(self, orderReceiver, coordinates):
        orderReceiver.robot.moveTo((coordinates["positionTO"]["positionX"], coordinates["positionTO"]["positionY"]))
        orderReceiver.wheelManager.moveTo((coordinates["positionTO"]["positionX"], coordinates["positionTO"]["positionY"]))
        if(coordinates["endOfPhase"] == "yes"):
            adjusterFactory = PositionAdjusterFactory()
            positionAdjuster = adjusterFactory.createState(coordinates["type"])
            positionAdjuster.getToTarget()
            if(coordinates["endOfCycle"] == "yes"):
                orderReceiver.setState(RefusingOrderState())