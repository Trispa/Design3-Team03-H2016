import json
import os
import sys
import threading
from thread import start_new_thread

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

def verifyIfMoving(path):
    print len(path)
    for index in range(0, len(path)):
        x = path[index].positionX
        y = path[index].positionY
        if(index+1 != len(path)):
            botInfo = dispatcher.getCurrentWorldInformation()
            botPositionX = botInfo["robotPosition"][0]
            botPositionY = botInfo["robotPosition"][1]
            while ((botPositionX > x + 10 or
                botPositionX < x - 10) and
                   (botPositionY > y + 10 or
                botPositionY < y - 10)):
                botInfo = dispatcher.getCurrentWorldInformation()
                botPositionX = botInfo["robotPosition"][0]
                botPositionY = botInfo["robotPosition"][1]
                print "not close enough"
            print "close enough"
            botInfo = dispatcher.getCurrentWorldInformation()
            jsonToSend = {"positionFROMx" : botInfo["robotPosition"][0],
                          "positionFROMy" : botInfo["robotPosition"][1],
                          "positionTOx" : path[index+1].positionX,
                          "positionTOy" : path[index+1].positionY,
                          "orientation":botInfo["robotOrientation"]}
            socketIO.emit("sendNextCoordinates", jsonToSend)
        else:
            print("sendingNextCoordinates")
            socketIO.emit("needNewCoordinates")


def sendNextCoordinates():
    path = dispatcher.handleCurrentSequencerState()
    sendInfo()
    verifyIfMoving(path)

def startRound():
    botPosition, botOrientation = dispatcher.initialiseWorldData()
    print("Bot is at : (" + str(botPosition[0]) + "," + str(botPosition[1]) + ")")
    print("Bot is orienting towards :" + str(botOrientation) + "degrees")
    botState = {"positionX": botPosition[0],
            "positionY": botPosition[1],
            "orientation": botOrientation}
    socketIO.emit("startSignalRobot",botState)

def sendInfo():
    print("asking for new informations")
    socketIO.emit('sendInfo', dispatcher.getCurrentWorldInformation())

def setTarget(manchesterInfo):
    dispatcher.setTarget(manchesterInfo['target'])


def setInterval(function, seconds):
    def func_wrapper():
        setInterval(function, seconds)
        function()
    timer = threading.Timer(seconds, func_wrapper)
    timer.start()
    return timer

setInterval(sendInfo, 5)
socketIO.on('needNewCoordinates', sendNextCoordinates)
socketIO.on('startSignal', startRound)
socketIO.on('sendManchesterInfo', setTarget)
socketIO.on("verifyIfMoving", verifyIfMoving)

socketIO.wait()

