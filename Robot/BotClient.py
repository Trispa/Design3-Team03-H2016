import json

from socketIO_client import SocketIO

import RobotMock


robot = RobotMock.RobotMock()

with open("../Shared/config.json") as json_data_file:
    config = json.load(json_data_file)


socketIO = SocketIO(config['url'], int(config['port']))

def launchSequence(*args):
    print("Bot going to charging station at : ", args[0])
    socketIO.emit('needTreasurePath', ("A", "cercle"))

def goToTreasure(*args):
    print("Bot going to treasure at : ", args[0])
    socketIO.emit('needTargetPath')

def goToTarget(*args):
    print("Bot going to target at : ", args[0])
    socketIO.emit('endSignal')


socketIO.emit('pythonClientStatus','Connected')
socketIO.on('goBot', launchSequence)
socketIO.on('sendingTreasurePath', goToTreasure)
socketIO.on('sendingTargetPath', goToTarget)

socketIO.wait()




