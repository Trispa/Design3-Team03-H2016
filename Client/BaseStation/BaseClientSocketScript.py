import json
import os
import sys
import cProfile

import time
from Logic.BaseStationDispatcher import BaseStationDispatcher
from WorldVision.worldVision import worldVision

sys.path.insert(1, "/Logic")
sys.path.append("/../../Shared")

from socketIO_client import SocketIO
from threading import Thread
dispatcher = BaseStationDispatcher(worldVision())

c = os.path.dirname(__file__)
configPath = os.path.join(c, "..", "..", "Shared", "config.json")
with open(configPath) as json_data_file:
    config = json.load(json_data_file)

socketIO = SocketIO(config['url'], int(config['port']))

def verifyIfMoving(path, nextSignal, angleToRotate):
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
            jsonToSend = {"botOrientation":botOrientation,
                          "angleToGo":angleToRotate,
                          "sequence":True}
            socketIO.emit(nextSignal, jsonToSend)

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
    path, nextSignal, angleToRotate = dispatcher.handleCurrentSequencerState()
    if(path != None and nextSignal != None):
        verifyIfMoving(path, nextSignal, angleToRotate)

def sendAlignPositionToChargingStationSignal():
    botInfo = dispatcher.getCurrentWorldInformation()
    jsonToSend = {"robotOrientation":botInfo['robotOrientation'],
                  "sequence":True}
    socketIO.emit('alignPositionToChargingStation', jsonToSend)

def sendAlignPositionToTreasureSignal():
    botInfo = dispatcher.getCurrentWorldInformation()
    jsonToSend = {"robotOrientation":botInfo['robotOrientation'],
                  "sequence":True}
    socketIO.emit('alignPositionToTreasure', jsonToSend)

def sendDetectTreasureSignal():
    botInfo = dispatcher.getCurrentWorldInformation()

    jsonToSend = {"botOrientation":botInfo['robotOrientation'],
                          "angleToGo":180,
                          "sequence":True}
    socketIO.emit('alignPositionToTreasure', jsonToSend)

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

def sendInformations():
    print("asking for new informations")
    socketIO.emit('sendInfo', dispatcher.getCurrentWorldInformation())

def setTarget(jsonTarget):
    dispatcher.setTargetOnMap(jsonTarget['target'])

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
        sendInformations()
        time.sleep(5)










#debug section
def verifyIfMovingDebug(path, nextSignal, angleToRotate):
    print("verify if moving")
    pixelRangeToSendNextCoordinates = 10
    for nodeBotIsGoingTo in range(0, len(path)):
        xPositionOfNodeThatBotIsGoingTo = path[nodeBotIsGoingTo].positionX
        yPositionOfNodeThatBotIsGoingTo = path[nodeBotIsGoingTo].positionY

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
        time.sleep(5)
        print "close enough"

        if(nodeBotIsGoingTo+1 != len(path)):
            print("sending bot to next coordinates")
            botInfo = dispatcher.getCurrentWorldInformation()
            jsonToSend = {"positionFROMx" : botInfo["robotPosition"][0],
                          "positionFROMy" : botInfo["robotPosition"][1],
                          "positionTOx" : path[nodeBotIsGoingTo+1].positionX,
                          "positionTOy" : path[nodeBotIsGoingTo+1].positionY,
                          "orientation":botInfo["robotOrientation"]}
            socketIO.emit("sendNextCoordinates", jsonToSend)

def debugSendBotToChargingStation():
    print "send bot to charging station debug launching"
    dispatcher.setSequencerStateToSendChargingStation()
    path, nextSignal, angleToRotate = dispatcher.handleCurrentSequencerState()
    verifyIfMovingDebug(path, nextSignal, angleToRotate)

def debugAlignBotToChargingStation():
    print "align bot to charging station debug launching"
    botInfo = dispatcher.getCurrentWorldInformation()
    jsonToSend = {"robotOrientation":botInfo['robotOrientation'],
                  "sequence":False}
    socketIO.emit('alignPositionToChargingStation', jsonToSend)

def debugSearchAllTreasure():
    print "search all treasures debug launching"

    dispatcher.setSequencerStateToDetectTreasures()
    path, nextSignal, angleToRotate = dispatcher.handleCurrentSequencerState()
    verifyIfMovingDebug(path, nextSignal, angleToRotate)
    botInfo = dispatcher.getCurrentWorldInformation()
    jsonToSend = {"botOrientation":botInfo['robotOrientation'],
                  "angleToGo":180,
                  "sequence":False}
    socketIO.emit(nextSignal, jsonToSend)

def debugSendBotToTreasure():
    print "send bot to treasure debug launching"

    dispatcher.setSequencerStateToSendToTreasure()
    path, nextSignal, angleToRotate = dispatcher.handleCurrentSequencerState()
    verifyIfMovingDebug(path, nextSignal, angleToRotate)

def debugAlignBotToTreasure():
    print "align bot to treasure debug launching"

    botInfo = dispatcher.getCurrentWorldInformation()
    jsonToSend = {"robotOrientation":botInfo['robotOrientation'],
                  "sequence":False}
    socketIO.emit('alignPositionToTreasure', jsonToSend)

def debugSendBotToTarget():
    print "send bot to target debug launching"

    dispatcher.setSequencerStateToSendToTarget()
    path, nextSignal, angleToRotate = dispatcher.handleCurrentSequencerState()
    verifyIfMovingDebug(path, nextSignal, angleToRotate)

def initializeWorld():
    print "initialize world debug launching"

    dispatcher.initialiseWorldData()

Thread(target=sendImageThread).start()

socketIO.on('needNewCoordinates', sendNextCoordinates)
socketIO.on('startSignal', startRound)
socketIO.on('sendManchesterInfo', setTarget)
socketIO.on("verifyIfMoving", verifyIfMoving)
socketIO.on("startFromTreasure", startFromTreasure)
socketIO.on("startFromTarget", startFromTarget)
socketIO.on('setTreasures', setTreasuresOnMap)


socketIO.on('debugSendBotToChargingStation', debugSendBotToChargingStation)
socketIO.on('debugAlignBotToChargingStation', debugAlignBotToChargingStation)
socketIO.on('debugSearchAllTreasure', debugSearchAllTreasure)
socketIO.on('debugSendBotToTreasure', debugSendBotToTreasure)
socketIO.on('debugAlignBotToTreasure', debugAlignBotToTreasure)
socketIO.on('debugSendBotToTarget', debugSendBotToTarget)
socketIO.on('initializeWorld', initializeWorld)
socketIO.on('rotateDoneToTreasure', sendAlignPositionToTreasureSignal)
socketIO.on('rotateDoneToChargingStation', sendAlignPositionToChargingStationSignal)
socketIO.on('rotateDoneToDetectTreasure', sendDetectTreasureSignal)
#cProfile.run('socketIO.wait()')
socketIO.wait()

