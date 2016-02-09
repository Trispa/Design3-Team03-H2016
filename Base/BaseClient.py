from socketIO_client import SocketIO
import base64
import json
import Logic.Sequencer

sequencer = Logic.Sequencer.Sequencer()

with open("../Shared/config.json") as json_data_file:
    config = json.load(json_data_file)

socketIO = SocketIO(config['url'], int(config['port']))

def clickGo():
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
    encoded = base64.b64encode(open("UI/style/img/Picture 1.jpg", "rb").read())
    return encoded

socketIO.emit('sendingImage', sendImage())
socketIO.on('launch', clickGo)
socketIO.on('needTreasurePath', sendTreasurePath)
socketIO.on('needTargetPath', sendTargetpath)

socketIO.wait()

