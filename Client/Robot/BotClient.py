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

def alignToTreasure():
    botDispatcher.alignToTreasure()
    socketIO.emit("needNewCoordinates")

def startRound(*args):
    print("start round")
    socketIO.emit("needNewCoordinates")

def endRound():
    print("end round")


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

socketIO.emit('sendBotClientStatus','Connected')
socketIO.emit('sendBotIP', get_ip_address('wlp3s0'))
#socketIO.on("alignToTreasure", alignToTreasure)
socketIO.on('sendNextCoordinates', needNewCoordinates)
socketIO.on('startSignalRobot', startRound)
socketIO.on('sendEndSignal', endRound)

socketIO.wait()