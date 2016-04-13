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
import subprocess
c = os.path.dirname(__file__)
configPath = os.path.join(c, "..", "..", "Shared", "config.json")

subprocess.call(['./cameraSettings.sh'])
with open(configPath) as json_data_file:
    config = json.load(json_data_file)
socketIO = SocketIO(config['url'], int(config['port']))
spc = SerialPortCommunicator()
botDispatcher = BotDispatcher(WheelManager(spc), Controller(), spc)



def goToNextPosition(data):
    print("heading toward next coordinates")
    botDispatcher.lastPositionGoneTo = (data['positionTOx'], data['positionTOy'])
    botDispatcher.followPath(data)


def startRound(json):
    print("start round")
    botDispatcher.lastPositionGoneTo = (json['positionX'], json['positionY'])
    socketIO.emit("needNewCoordinates")

def alignToTreasure(json):
    if(json['sequence']):
        botDispatcher.setRobotOrientation(json['botOrientation'], json["angleToGo"])
    botDispatcher.alignToTreasure(Controller())
    if(botDispatcher.lastPositionGoneTo[0] - 100 == 0):
        botDispatcher.getRobotBackOnMapWhenOutOfBound()
    if(json['sequence']):
        socketIO.emit("needNewCoordinates")

def alignToChargingStation(json):
    botDispatcher.setRobotOrientation(json['botOrientation'], json["angleToGo"])
    botDispatcher.alignToChargingStation()
    botDispatcher.serialPortCommunicatorIsReadByManchester = True
    readManchester()
    botDispatcher.serialPortCommunicatorIsReadByManchester = False
    voltage = spc.readConsensatorVoltage()
    while(voltage <= 3.5):
        voltage = spc.readConsensatorVoltage()
        print "Tension : ", voltage
        time.sleep(1)
    botDispatcher.getRobotBackOnMapAfterCharging()
    if(json['sequence']):
        print ('asking new commands')
        socketIO.emit("needNewCoordinates")

def alignToTarget(json):
    botDispatcher.setRobotOrientation(json['botOrientation'], json['angleToGo'])
    botDispatcher.alignToTargetIslandTest(json['targetColor'])
    socketIO.emit("sendEndSignal")

def endRound():
    print("end round")

def detectTreasure(json):
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

def sendBotVoltage():
    while(True):
        voltage = spc.getTensionCondensateur()
        socketIO.emit('sendVoltage', voltage)
        print "send bot voltage"
        time.sleep(5)


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
socketIO.on('debugAlignToTarget', alignToTarget)


socketIO.wait()
