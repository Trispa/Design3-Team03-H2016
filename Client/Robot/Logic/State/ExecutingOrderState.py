
class ExecutingOrderState():
    def __init__(self):
        self.sendingSignal = "needNewCoordinates"


    def handle(self, orderReceiver, coordinates):
        orderReceiver.robot.moveTo(coordinates)
        orderReceiver.wheelManager.moveTo(coordinates)
        orderReceiver.robot.botInfo['voltage'] = "12V"
        orderReceiver.robot.botInfo['decodedCharacter'] = "A"
        orderReceiver.robot.botInfo['target'] = "cercle"

