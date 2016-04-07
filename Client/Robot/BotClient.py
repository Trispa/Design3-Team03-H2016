import json
import os
import socket
import struct
from Client.Robot.Mechanical.maestro import Controller
from Client.Robot.Mechanical.SerialPortCommunicator import SerialPortCommunicator
import fcntl
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
    botDispatcher.lastPositionGoneTo = (data['positionTOX'], data['positionTOY'])
    botDispatcher.followPath(data)


def startRound(json):
    print("start round")
    botDispatcher.lastPositionGoneTo = (json['positionX'], json['positionY'])
    socketIO.emit("needNewCoordinates")

def alignToTreasure(json):
    if(json['sequence']):
        angleToGetForChargingStation = botDispatcher.treasureAngle
        minimumAngleDifferenceToRotate = 3
        if(abs(json['robotOrientation'] - angleToGetForChargingStation) > minimumAngleDifferenceToRotate):
            botDispatcher.setRobotOrientation(json['robotOrientation'], botDispatcher.treasureAngle)
    botDispatcher.alignToTreasure(Controller())
    if(botDispatcher.lastPositionGoneTo[0] == 0):
        botDispatcher.getRobotBackOnMapWhenOutOfBound()
    if(json['sequence']):
        socketIO.emit("needNewCoordinates")


def rotateToChargingStation(json):
    botDispatcher.setRobotOrientation(float(json['botOrientation']), float(json['angleToGo']))
    socketIO.emit('rotateDoneToChargingStation', json["sequence"])

def rotateToTreasure(json):
    botDispatcher.treasureAngle =  float(json['angleToGo'])
    botDispatcher.setRobotOrientation(float(json['botOrientation']), float(json['angleToGo']))
    socketIO.emit('rotateDoneToTreasure')

def rotateToDetectTreasure(json):
    botDispatcher.setRobotOrientation(json['botOrientation'],json['angleToGo'])
    socketIO.emit('rotateDoneToDetectTreasure')


def alignToChargingStation(json):
    angleToGetForChargingStation = 270
    minimumAngleDifferenceToRotate = 3
    if(abs(json['robotOrientation'] - angleToGetForChargingStation) > minimumAngleDifferenceToRotate):
        botDispatcher.setRobotOrientation(json['robotOrientation'], angleToGetForChargingStation)
    botDispatcher.alignToChargingStation()
    readManchester()
    voltage = spc.readConsensatorVoltage()
    while(voltage <= 3.0):
        voltage = spc.readConsensatorVoltage()
        print "Tension : ", voltage
        time.sleep(1)
    botDispatcher.getRobotBackOnMapAfterCharging()
    time.sleep(20)
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

socketIO.emit('sendBotClientStatus','Connected')
socketIO.emit('sendBotIP', get_ip_address('wlp4s0'))

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
