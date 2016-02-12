import base64
import json

from Logic.Sequencer import Sequencer as seq

sequencer = seq()

from socketIO_client import SocketIO

with open("../../Shared/config.json") as json_data_file:
    config = json.load(json_data_file)

socketIO = SocketIO(config['url'], int(config['port']))

def sendingNextCoordinates():
    print("Sending orders")
    socketIO.emit("sendingNextCoordinates", sequencer.handleCurrentState())

def sendImage():
    print("asking for new images")
    encoded = base64.b64encode(open("../UI/style/img/Picture 1.jpg", "rb").read())
    socketIO.emit('sendingImage', encoded)

socketIO.on('needNewImage', sendImage)
socketIO.on('needNewCoordinates', sendingNextCoordinates)

socketIO.wait()

