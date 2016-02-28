import json


from socketIO_client import SocketIO
from Logic.RobotMock import RobotMock
from Logic.ReferentialConverter import ReferentialConverter

with open("../../Shared/config.json") as json_data_file:
    config = json.load(json_data_file)
socketIO = SocketIO(config['url'], int(config['port']))
#referentialConverter = ReferentialConverter(positionRobot, orientation);
#wheelManager = WheelManager()

robot = RobotMock()
def needNewCoordinates(*args):
    print("Bot going to " + args[0]["type"] + " at : (" + args[0]["position"]["positionX"] + " " + args[0]["position"]["positionY"] + ")")
    #pointConverted = referentialConverter.convertWorldToRobot((int(args[0]["position"]["positionX"]), int(args[0]["position"]["positionY"]))
    pointConverted = (int(args[0]["position"]["positionX"]), int(args[0]["position"]["positionY"]))
    robot.moveTo(pointConverted)
    #wheelManager.moveTo(pointConverted)
    if(args[0]["type"] == "target"):
        robot.botInfo['voltage'] = "N/A"
        robot.botInfo['decodedCharacter'] = "N/A"
        robot.botInfo['target'] = "N/A"
        socketIO.emit('sendEndSignal')
    else:
        robot.botInfo['voltage'] = "12V"
        robot.botInfo['decodedCharacter'] = "A"
        robot.botInfo['target'] = "cercle"
        socketIO.emit('needNewCoordinates')

def sendInfo():
    robot.botInfo['position'] = "(" + str(robot.positionX) + "," + str(robot.positionY) + ")"
    robot.botInfo['orientation'] = str(robot.orientation)
    socketIO.emit('sendInfo', robot.botInfo)

socketIO.emit('sendBotClientStatus','Connected')
socketIO.on('needUpdatedInfo', sendInfo)
socketIO.on('sendNextCoordinates', needNewCoordinates)

socketIO.wait()




