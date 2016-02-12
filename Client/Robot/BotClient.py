import json

from socketIO_client import SocketIO
from Logic.RobotMock import RobotMock

with open("../../Shared/config.json") as json_data_file:
    config = json.load(json_data_file)

robot = RobotMock()


socketIO = SocketIO(config['url'], int(config['port']))

def needNewCoordinates(*args):
    print("Bot going to " + args[0]["type"] + " at : (" + args[0]["position"]["positionX"] + " " + args[0]["position"]["positionY"] + ")")
    robot.move((int(args[0]["position"]["positionX"]), int(args[0]["position"]["positionY"])))
    if(args[0]["type"] == "target"):
        socketIO.emit('endSignal')
    else:
        robot.tension = "12V"
        socketIO.emit('needNewCoordinates',{"decodedCharacter":"A", "target":"cercle"})

def sendVoltage():
        socketIO.emit('sendingVoltage', robot.tension)



socketIO.emit('botClientStatus','Connected')
socketIO.on('needUpdatedInfo', sendVoltage)
socketIO.on('sendingNextCoordinates', needNewCoordinates)

socketIO.wait()




