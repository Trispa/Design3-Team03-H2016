import json
import os

from socketIO_client import SocketIO
from Logic.BotDispatcher import BotDispatcher
from Client.Robot.Logic.Deplacement.WheelManager import WheelManager

from Logic.RobotMock import RobotMock
from Mechanical.MoteurRoue import MoteurRoue

c = os.path.dirname(__file__)
configPath = os.path.join(c, "..", "..", "Shared", "config.json")

with open(configPath) as json_data_file:
    config = json.load(json_data_file)
socketIO = SocketIO(config['url'], int(config['port']))

#orderReceiver = BotDispatcher(RobotMock())
botDispatcher = BotDispatcher(WheelManager(MoteurRoue()))

def needNewCoordinates(*args):
    print("heading toward next coordinates")
    botDispatcher.handleCurrentState(args[0])
    whichObstacleNextIsNeeded = int(args[0]["index"]) + 1
    print(botDispatcher.state.__class__)
    socketIO.emit(botDispatcher.state.sendingSignal, {"index" : str(whichObstacleNextIsNeeded)})

def startRound(*args):
    print("start round")
    botDispatcher.acceptOrders()
    socketIO.emit(botDispatcher.state.sendingSignal, {"index": "0"})

def endRound():
    print("end round")
    botDispatcher.refuseOrders()

socketIO.emit('sendBotClientStatus','Connected')
socketIO.on('sendNextCoordinates', needNewCoordinates)
socketIO.on('startSignalRobot', startRound)
socketIO.on('sendEndSignal', endRound)

socketIO.wait()