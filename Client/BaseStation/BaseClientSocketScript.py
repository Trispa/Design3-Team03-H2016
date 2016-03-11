import base64
import json
import sys
import cv2
import threading
import os
from BaseClient import BaseClient
sys.path.insert(1, "/Logic")
sys.path.append("/../../Shared")

from socketIO_client import SocketIO

bob = BaseClient()

c = os.path.dirname(__file__)
configPath = os.path.join(c, "..", "..", "Shared", "config.json")
with open(configPath) as json_data_file:
    config = json.load(json_data_file)

socketIO = SocketIO(config['url'], int(config['port']))

def sendNextCoordinates(*args):
    print("Sending next coordinates")
    value =  bob.handleCurrentSequencerState(args[0]["index"])
    print value
    socketIO.emit("sendNextCoordinates",value)

def startRound():
    botState = {"positionX":"0",
                "positionY":"0",
                "orientation":"0"}
    print("sending start signal robot")
    bob.initialiseWorldData()
    print("finish initializing world")
    socketIO.emit("startSignalRobot",botState)

def sendImage():
    print("asking for new images")
    socketIO.emit('sendImage', bob.getCurrentWorldImage())

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

socketIO.wait()

