import base64
import json

from Logic.Sequencer import Sequencer as seq
sequencer = seq()

from socketIO_client import SocketIO

with open("../../../Shared/config.json") as json_data_file:
    config = json.load(json_data_file)

socketIO = SocketIO(config['url'], int(config['port']))

def clickGo():
    print("Go button clicked")
    print("Sending bot to charging station")
    socketIO.emit("goBot", sequencer.handleCurrentState())

def sendTreasurePath():
    treasureCoordinate = sequencer.handleCurrentState()
    print("Sending bot to treasure")
    socketIO.emit('sendingTreasurePath', treasureCoordinate)

def sendTargetpath():
    targetCoordinate =  sequencer.handleCurrentState()
    print("Sending bot to target")
    socketIO.emit('sendingTargetPath', targetCoordinate)

def sendImage():
    print("asking for new images")
    encoded = base64.b64encode(open("../UI/style/img/Picture 1.jpg", "rb").read())
    socketIO.emit('sendingImage', encoded)

socketIO.on('needNewImage', sendImage)
socketIO.on('launch', clickGo)
socketIO.on('needTreasurePath', sendTreasurePath)
socketIO.on('needTargetPath', sendTargetpath)

socketIO.wait()

