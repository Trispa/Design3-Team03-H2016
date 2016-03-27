import json
import os

from socketIO_client import SocketIO

from Client.Robot.Logic.Deplacement.WheelManager import WheelManager

from Logic.BotDispatcher import BotDispatcher

c = os.path.dirname(__file__)
configPath = os.path.join(c, "..", "..", "Shared", "config.json")

with open(configPath) as json_data_file:
    config = json.load(json_data_file)
socketIO = SocketIO(config['url'], int(config['port']))

botDispatcher = BotDispatcher(WheelManager())

def needNewCoordinates(data):
    print("heading toward next coordinates")
    botDispatcher.followPath(data)

def alignToTreasure():
    botDispatcher.alignToTreasure()
    socketIO.emit("needNewCoordinates")

def startRound(*args):
    print("start round")
    socketIO.emit("needNewCoordinates")

def endRound():
    print("end round")

socketIO.emit('sendBotClientStatus','Connected')
#socketIO.on("alignToTreasure", alignToTreasure)
socketIO.on('sendNextCoordinates', needNewCoordinates)
socketIO.on('startSignalRobot', startRound)
socketIO.on('sendEndSignal', endRound)

socketIO.wait()