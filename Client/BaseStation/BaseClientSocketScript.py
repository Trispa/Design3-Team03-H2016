import json
import os
import sys
import threading
import time
from Logic.BaseStationDispatcher import BaseStationDispatcher

sys.path.insert(1, "/Logic")
sys.path.append("/../../Shared")

from socketIO_client import SocketIO
from threading import Thread
dispatcher = BaseStationDispatcher()

c = os.path.dirname(__file__)
configPath = os.path.join(c, "..", "..", "Shared", "config.json")
with open(configPath) as json_data_file:
    config = json.load(json_data_file)

socketIO = SocketIO(config['url'], int(config['port']))

def verifyIfMoving(path, nextSignal):
    pixelRangeToSendNextCoordinates = 8
    for nodeBotIsGoingTo in range(0, len(path)):
        xPositionOfNodeThatBotIsGoingTo = path[nodeBotIsGoingTo].positionX
        yPositionOfNodeThatBotIsGoingTo = path[nodeBotIsGoingTo].positionY
        if(nodeBotIsGoingTo+1 != len(path)):
            botInfo = dispatcher.getCurrentWorldInformation()
            botPositionX = botInfo["robotPosition"][0]
            botPositionY = botInfo["robotPosition"][1]
            while ((botPositionX > xPositionOfNodeThatBotIsGoingTo + pixelRangeToSendNextCoordinates or
                botPositionX < xPositionOfNodeThatBotIsGoingTo - pixelRangeToSendNextCoordinates) and
                   (botPositionY > yPositionOfNodeThatBotIsGoingTo + pixelRangeToSendNextCoordinates or
                botPositionY < yPositionOfNodeThatBotIsGoingTo - pixelRangeToSendNextCoordinates)):
                botInfo = dispatcher.getCurrentWorldInformation()
                botPositionX = botInfo["robotPosition"][0]
                botPositionY = botInfo["robotPosition"][1]
                print "not close enough"
            print "close enough"
            time.sleep(5)
            if(nodeBotIsGoingTo+1 != len(path)):
                socketIO.emit(nextSignal)
            else:
                botInfo = dispatcher.getCurrentWorldInformation()
                jsonToSend = {"positionFROMx" : botInfo["robotPosition"][0],
                              "positionFROMy" : botInfo["robotPosition"][1],
                              "positionTOx" : path[nodeBotIsGoingTo+1].positionX,
                              "positionTOy" : path[nodeBotIsGoingTo+1].positionY,
                              "orientation":botInfo["robotOrientation"]}
                socketIO.emit("sendNextCoordinates", jsonToSend)


def sendNextCoordinates():
    path, nextSignal = dispatcher.handleCurrentSequencerState()
    if(path != None and nextSignal != None):
        Thread(target=verifyIfMoving(path, nextSignal)).start()


def startRound():
    dispatcher.startFromBegining()
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

def startFromTreasure():
    dispatcher.startFromTreasure()
    startRound()

def startFromTarget():
    dispatcher.startFromTarget()
    startRound()

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
socketIO.on("startFromTreasure", startFromTreasure)
socketIO.on("startFromTarget", startFromTarget)

socketIO.wait()

