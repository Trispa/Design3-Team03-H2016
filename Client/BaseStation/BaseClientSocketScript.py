import json
import os
import sys
import threading

from Logic.BaseStationDispatcher import BaseStationDispatcher

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
    botPosition, botOrientation = dispatcher.initialiseWorldData()

    print("Bot is at : (" + str(botPosition[0]) + "," + str(botPosition[1]) + ")")
    print("Bot is orienting towards :" + str(botOrientation) + "degrees")

    botState = {"positionX": botPosition[0],
            "positionY": botPosition[1],
            "orientation": botOrientation}
    socketIO.emit("startSignalRobot",botState)

def sendImage():
    print("asking for new images")
    socketIO.emit('sendImage', dispatcher.getCurrentWorldImage())

def sendToChargingStation():
    dispatcher.initialiseWorldData()
    dispatcher.sendToChargingStation()
    startRound()
    socketIO.emit("sendNextCoordinates",dispatcher.handleCurrentSequencerState(0))

def sendToTreasure():
    dispatcher.initialiseWorldData()
    dispatcher.sendToTreasure()
    startRound()
    socketIO.emit("sendNextCoordinates",dispatcher.handleCurrentSequencerState(0))

def setTarget(manchesterInfo):
    dispatcher.setTarget(manchesterInfo['target'])


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
socketIO.on('sendToChargingStation', sendToChargingStation)
socketIO.on('sendToTreasure', sendToTreasure)
socketIO.on('sendManchesterInfo', setTarget)

socketIO.wait()

