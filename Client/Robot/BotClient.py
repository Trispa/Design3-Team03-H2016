import json
import os
import socket
import fcntl
import struct

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


def startRound(*args):
    print("start round")
    socketIO.emit("needNewCoordinates")

def alignToTreasure():
    botDispatcher.alignToTreasure()
    socketIO.emit("needNewCoordinates")
def alignToChargingStation():
    botDispatcher.alignToTreasure()
    readManchester()
    socketIO.emit("needNewCoordinates")
def alignToTarget():
    #TODO code pour s'enligner a la cible
    socketIO.emit("needNewCoordinates")

def endRound():
    print("end round")

def detectTreasure():
    anglesList = botDispatcher.detectTreasure()
    socketIO.emit('setTreasures', anglesList)
    socketIO.emit('needNewCoordinates')

def readManchester():
    character = botDispatcher.readManchester()
    socketIO.emit("sendManchesterCode", character)

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

socketIO.emit('sendBotClientStatus','Connected')
socketIO.emit('sendBotIP', get_ip_address('wlp4s0'))

socketIO.on('sendNextCoordinates', needNewCoordinates)
socketIO.on('startSignalRobot', startRound)
socketIO.on('sendEndSignal', endRound)
socketIO.on('readManchester', readManchester)
socketIO.on("alignPositionToChargingStation", alignToChargingStation)
socketIO.on("alignPositionToTreasure", alignToTreasure)
socketIO.on("alignPositionToTarget", alignToTarget)
socketIO.on("detectTreasure", detectTreasure)

socketIO.wait()