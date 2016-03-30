import json
import os
import sys
import cProfile
from threading import current_thread
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
    print("verify if moving")
    pixelRangeToSendNextCoordinates = 10
    for nodeBotIsGoingTo in range(0, len(path)):
        xPositionOfNodeThatBotIsGoingTo = path[nodeBotIsGoingTo].positionX
        yPositionOfNodeThatBotIsGoingTo = path[nodeBotIsGoingTo].positionY

        botInfo = dispatcher.getCurrentWorldInformation()

        botPositionX = botInfo["robotPosition"][0]
        botPositionY = botInfo["robotPosition"][1]
        botOrientation = botInfo["robotOrientation"]

        while ((botPositionX > xPositionOfNodeThatBotIsGoingTo + pixelRangeToSendNextCoordinates or
            botPositionX < xPositionOfNodeThatBotIsGoingTo - pixelRangeToSendNextCoordinates) and
               (botPositionY > yPositionOfNodeThatBotIsGoingTo + pixelRangeToSendNextCoordinates or
            botPositionY < yPositionOfNodeThatBotIsGoingTo - pixelRangeToSendNextCoordinates)):
            botInfo = dispatcher.getCurrentWorldInformation()
            botPositionX = botInfo["robotPosition"][0]
            botPositionY = botInfo["robotPosition"][1]
            botOrientation = botInfo["robotOrientation"]
            print "not close enough"
        time.sleep(5)
        print "close enough"

        if(nodeBotIsGoingTo+1 == len(path)):
            print("emitting" + nextSignal)
            socketIO.emit(nextSignal, botOrientation)

        else:
            print("sending bot to next coordinates")
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
        verifyIfMoving(path, nextSignal)

def alignPositionToChargingStation():
    botInfo = dispatcher.getCurrentWorldInformation()
    socketIO.emit('alignPositionToChargingStation', botInfo['robotOrientation'])

def startRound():
    botPosition, botOrientation = dispatcher.initialiseWorldData()
    dispatcher.startFromBegining()
    startSignal(botPosition, botOrientation)

def startSignal(botPosition, botOrientation):
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
    print("start from treasure launch")
    socketIO.emit("sendManchesterCode", "A")
    botPosition, botOrientation = dispatcher.initialiseWorldData()
    dispatcher.startFromTreasure()
    startSignal(botPosition, botOrientation)

def startFromTarget():
    botPosition, botOrientation = dispatcher.initialiseWorldData()
    dispatcher.startFromTarget()
    startSignal(botPosition, botOrientation)

def setTreasuresOnMap(data):
    print("settingTreasuresOnMap")
    dispatcher.setTreasuresOnMap(data)

def sendImageThread():
    while True:
        sendInfo()
        time.sleep(5)

def getRobotAngle():
    botInfo = dispatcher.getCurrentWorldInformation()
    socketIO.emit("returnRobotAngle",botInfo["robotOrientation"])

Thread(target=sendImageThread).start()

socketIO.on('needNewCoordinates', sendNextCoordinates)
socketIO.on('startSignal', startRound)
socketIO.on('sendManchesterInfo', setTarget)
socketIO.on("verifyIfMoving", verifyIfMoving)
socketIO.on("startFromTreasure", startFromTreasure)
socketIO.on("startFromTarget", startFromTarget)
socketIO.on('setTreasures', setTreasuresOnMap)
socketIO.on("getRobotAngle", getRobotAngle)
socketIO.on('rotateDoneToChargingStation', alignPositionToChargingStation)
#cProfile.run('socketIO.wait()')
socketIO.wait()

