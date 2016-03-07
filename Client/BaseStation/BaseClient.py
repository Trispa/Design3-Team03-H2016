import base64
import json
import sys
import threading
import os

from WorldVision.worldVision import worldVision

sys.path.insert(1, "/Logic")
sys.path.append("/../../Shared")

from Logic.Sequencer import Sequencer as seq

sequencer = seq()

from socketIO_client import SocketIO

c = os.path.dirname(__file__)
configPath = os.path.join(c, "..", "..", "Shared", "config.json")
world = worldVision()

with open(configPath) as json_data_file:
    config = json.load(json_data_file)

socketIO = SocketIO(config['url'], int(config['port']))

def sendNextCoordinates(*args):
    print("Sending next coordinates")
    socketIO.emit("sendNextCoordinates", sequencer.handleCurrentState(args[0]["index"]))

def startRound():
    botState = {"positionX":"0",
                "positionY":"0",
                "orientation":"0"}
    print("sending start signal robot")
    socketIO.emit("startSignalRobot",botState)

def sendImage():
    print("asking for new images")
    image = world.saveImage()
    socketIO.emit('sendImage', image)

def setInterval(function, seconds):
    def func_wrapper():
        setInterval(function, seconds)
        function()
    timer = threading.Timer(seconds, func_wrapper)
    timer.start()
    return timer

setInterval(sendImage, 5)
socketIO.on('needNewInfo', sendImage)
socketIO.on('needNewCoordinates', sendNextCoordinates)
socketIO.on('startSignal', startRound)

socketIO.wait()

