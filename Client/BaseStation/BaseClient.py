import base64
import json

from Logic.Sequencer import Sequencer as seq
from WorldVision.worldVision import worldVision

sequencer = seq()

from socketIO_client import SocketIO

with open("../../Shared/config.json") as json_data_file:
    config = json.load(json_data_file)

socketIO = SocketIO(config['url'], int(config['port']))

def sendingNextCoordinates(*args):
    print("Sending orders")
    socketIO.emit("sendingNextCoordinates", sequencer.handleCurrentState())

def sendImage():
    print("asking for new images")
    world = worldVision()
    world.saveImage()
    encoded = base64.b64encode(open("../../Shared/worldVision.jpg", "rb").read())
    socketIO.emit('sendingImage', encoded)

socketIO.on('needUpdatedInfo', sendImage)
socketIO.on('needNewCoordinates', sendingNextCoordinates)

socketIO.wait()

