import json

from socketIO_client import SocketIO

with open("../../Shared/config.json") as json_data_file:
    config = json.load(json_data_file)


socketIO = SocketIO(config['url'], int(config['port']))

def needNewCoordinates(*args):
    print("Bot going to " + args[0]["type"] + " at : (" + args[0]["position"]["positionX"] + " " + args[0]["position"]["positionY"] + ")")
    if(args[0]["type"] == "target"):
        socketIO.emit('endSignal')
    else:
        socketIO.emit('needNewCoordinates', ("A", "cercle"))

socketIO.emit('botClientStatus','Connected')
socketIO.on('sendingNextCoordinates', needNewCoordinates)

socketIO.wait()




