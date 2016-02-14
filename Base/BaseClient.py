from socketIO_client import SocketIO, LoggingNamespace
import base64
import json

with open("../Shared/config.json") as json_data_file:
    config = json.load(json_data_file)

def sendImage():
    encoded = base64.b64encode(open("UI/style/img/Picture 1.jpg", "rb").read())
    print(encoded)
    return encoded

with SocketIO(config['url'], int(config['port']), LoggingNamespace) as socketIO:
    socketIO.emit('sendingImage', sendImage())
    socketIO.wait()