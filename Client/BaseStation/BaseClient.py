import base64
import json
from Logic.Sequencer import Sequencer as seq
from WorldVision.worldVision import worldVision
import threading

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

sequencer = seq()

from socketIO_client import SocketIO

with open("../../Commun/config.json") as json_data_file:
    config = json.load(json_data_file)

socketIO = SocketIO(config['url'], int(config['port']))

def sendNextCoordinates(*args):
    print("Sending next coordinates")
    socketIO.emit("sendNextCoordinates", sequencer.handleCurrentState())

def startRound():
    botState = {"positionX":"0",
                "positionY":"0",
                "orientation":"0"}
    print("sending start signal robot")
    socketIO.emit("startSignalRobot",botState)

def sendImage():
    print("asking for new images")
    world = worldVision()
    world.saveImage()
    encoded = base64.b64encode(open("../../Commun/worldImage.jpg", "rb").read())
    socketIO.emit('sendImage', encoded)

set_interval(sendImage, 5)

socketIO.on('needNewCoordinates', sendNextCoordinates)
socketIO.on('startSignal', startRound)

socketIO.wait()

