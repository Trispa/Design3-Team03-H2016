import json
from socketIO_client import SocketIO
from Logic.BotDispatcher import BotDispatcher
from Logic.WheelManager import WheelManager
from Logic.RobotMock import RobotMock
from Mechanical.MoteurRoue import MoteurRoue
import os

c = os.path.dirname(__file__)
configPath = os.path.join(c, "..", "..", "Shared", "config.json")

with open(configPath) as json_data_file:
    config = json.load(json_data_file)
socketIO = SocketIO(config['url'], int(config['port']))
orderReceiver = BotDispatcher(RobotMock())
#orderReceiver = BotDispatcher(RobotMock(), WheelManager(MoteurRoue()))

def needNewCoordinates(*args):
    print("heading toward next coordinates")
    orderReceiver.handleCurrentState(args[0])
    whichObstacleNextIsNeeded = int(args[0]["index"]) + 1
    print(orderReceiver.state.__class__)
    socketIO.emit(orderReceiver.state.sendingSignal, {"index" : str(whichObstacleNextIsNeeded)})

def startRound(*args):
    print("start round")
    orderReceiver.acceptOrders()
    orderReceiver.initializeRobot(int(args[0]["positionX"]), int(args[0]["positionY"]), int(args[0]["orientation"]))
    socketIO.emit(orderReceiver.state.sendingSignal, {"index": "0"})

def endRound():
    print("end round")
    orderReceiver.refuseOrders()

socketIO.emit('sendBotClientStatus','Connected')
socketIO.on('sendNextCoordinates', needNewCoordinates)
socketIO.on('startSignalRobot', startRound)
socketIO.on('sendEndSignal', endRound)

socketIO.wait()




