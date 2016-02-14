from socketIO_client import SocketIO, LoggingNamespace
import json

with open("../Shared/config.json") as json_data_file:
    config = json.load(json_data_file)

with SocketIO(config['url'], int(config['port']), LoggingNamespace) as socketIO:
    socketIO.emit('pythonClientStatus','Connected')
    socketIO.wait()