import json
import os
import sys
import threading

from Client.BaseStation.Logic.BaseStationDispatcher import BaseStationDispatcher

sys.path.insert(1, "/Logic")
sys.path.append("/../../Shared")

from socketIO_client import SocketIO

dispatcher = BaseStationDispatcher()

c = os.path.dirname(__file__)
configPath = os.path.join(c, "..", "..", "Shared", "config.json")
with open(configPath) as json_data_file:
    config = json.load(json_data_file)

socketIO = SocketIO(config['url'], int(config['port']))

def sendNextCoordinates(*args):
    print("Sending next coordinates")
    socketIO.emit("sendNextCoordinates",dispatcher.handleCurrentSequencerState(args[0]["index"]))

def startRound():
    botState = {"positionX":"0",
                "positionY":"0",
                "orientation":"0"}
    dispatcher.initialiseWorldData()
    socketIO.emit("startSignalRobot",botState)

def sendImage():
    print("asking for new images")
    socketIO.emit('sendImage', dispatcher.getCurrentWorldImage())

def setInterval(function, seconds):
    def func_wrapper():
        setInterval(function, seconds)
        function()
    timer = threading.Timer(seconds, func_wrapper)
    timer.start()
    return timer

setInterval(sendImage, 5)
socketIO.on('needNewCoordinates', sendNextCoordinates)
socketIO.on('startSignal', startRound)

socketIO.wait()

