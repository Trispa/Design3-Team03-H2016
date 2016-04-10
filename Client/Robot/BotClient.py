import json
import os
import socket
import struct
from Client.Robot.Mechanical.maestro import Controller
from Client.Robot.Mechanical.SerialPortCommunicator import SerialPortCommunicator
import fcntl
from threading import Thread
from socketIO_client import SocketIO
import time
from Client.Robot.Movement.WheelManager import WheelManager
from Logic.BotDispatcher import BotDispatcher

c = os.path.dirname(__file__)
configPath = os.path.join(c, "..", "..", "Shared", "config.json")

with open(configPath) as json_data_file:
    config = json.load(json_data_file)
socketIO = SocketIO(config['url'], int(config['port']))
spc = SerialPortCommunicator()
botDispatcher = BotDispatcher(WheelManager(spc), Controller(), spc)



def goToNextPosition(data):
    print("heading toward next coordinates")
    botDispatcher.followPath(data)


def startRound(*args):
    print("start round")
    socketIO.emit("needNewCoordinates")

def alignToTreasure(json):
    if(json['sequence']):
        angleToGetForChargingStation = botDispatcher.treasureAngle
        minimumAngleDifferenceToRotate = 3
        if(abs(json['robotOrientation'] - angleToGetForChargingStation) > minimumAngleDifferenceToRotate):
            botDispatcher.setRobotOrientation(json['robotOrientation'], botDispatcher.treasureAngle)
    botDispatcher.alignToTreasure(Controller())
    if(json['sequence']):
        socketIO.emit("needNewCoordinates")


def rotateToChargingStation(json):
   # botDispatcher.setRobotOrientation(float(json['botOrientation']), float(json['angleToGo']))
    socketIO.emit('rotateDoneToChargingStation', json["sequence"])

def rotateToTreasure(json):
    botDispatcher.treasureAngle =  float(json['angleToGo'])
   # botDispatcher.setRobotOrientation(float(json['botOrientation']), float(json['angleToGo']))
    socketIO.emit('rotateDoneToTreasure')

def rotateToDetectTreasure(json):
    #botDispatcher.setRobotOrientation(json['botOrientation'],json['angleToGo'])
    socketIO.emit('rotateDoneToDetectTreasure')


def alignToChargingStation(json):
    angleToGetForChargingStation = 270
    minimumAngleDifferenceToRotate = 3
    if(abs(json['robotOrientation'] - angleToGetForChargingStation) > minimumAngleDifferenceToRotate):
        botDispatcher.setRobotOrientation(json['robotOrientation'], angleToGetForChargingStation)
    botDispatcher.alignToChargingStation()
    botDispatcher.serialPortCommunicatorIsReadByManchester = True
    readManchester()
    botDispatcher.serialPortCommunicatorIsReadByManchester = False
    voltage = botDispatcher.botVoltage
    while(voltage <= 3.0):
        voltage = botDispatcher.botVoltage
        print "Tension : ", voltage
        time.sleep(1)
    botDispatcher.getRobotBackOnMap()
    if(json['sequence']):
        print ('asking new commands')
        socketIO.emit("needNewCoordinates")

def alignToTarget(json):
    botDispatcher.setRobotOrientation(json['botOrientation'], json['angleToGo'])
    botDispatcher.alignToTargetIsland()
    socketIO.emit("needNewCoordinates")

def endRound():
    print("end round")

def detectTreasure(json):
    minimumAngleDifferenceToRotate = 3
    if(abs(json['botOrientation'] - json['angleToGo']) > minimumAngleDifferenceToRotate):
        botDispatcher.setRobotOrientation(json['botOrientation'], json['angleToGo'])
    anglesList = botDispatcher.detectTreasure()
    socketIO.emit('setTreasures', anglesList)
    if(json['sequence']):
        socketIO.emit('needNewCoordinates')

def readManchester():
    character = botDispatcher.readManchester()
    socketIO.emit("sendManchesterCode", character)

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,
        struct.pack('256s', ifname[:15])
    )[20:24])

def getBotVoltage():
    while(True):
        if not botDispatcher.serialPortCommunicatorIsReadByManchester:
            botDispatcher.botVoltage = spc.readConsensatorVoltage()
        time.sleep(1)

def sendBotVoltage():
    while(True):
        socketIO.emit('sendVoltage', botDispatcher.botVoltage)
        print "send bot voltage"
        time.sleep(5)


Thread(target=getBotVoltage).start()
Thread(target=sendBotVoltage).start()


socketIO.emit('sendBotClientStatus','Connected')
socketIO.emit('sendBotIP', get_ip_address('wlp4s0'))
socketIO.emit('sendVoltage', botDispatcher.botVoltage)

socketIO.on('sendNextCoordinates', goToNextPosition)
socketIO.on('startSignalRobot', startRound)
socketIO.on('sendEndSignal', endRound)
socketIO.on('readManchester', readManchester)
socketIO.on("alignPositionToChargingStation", alignToChargingStation)
socketIO.on("alignPositionToTreasure", alignToTreasure)
socketIO.on("alignPositionToTarget", alignToTarget)
socketIO.on("detectTreasure", detectTreasure)
socketIO.on('rotateToChargingStation', rotateToChargingStation)
socketIO.on('rotateToTreasure', rotateToTreasure)
socketIO.on('rotateToDetectTreasure', rotateToDetectTreasure)
socketIO.on('debugAlignToTarget', alignToTarget)

socketIO.wait()
