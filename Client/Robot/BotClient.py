import json

from Logic.OrderReceiver import OrderReceiver
from socketIO_client import SocketIO
from Logic.RobotMock import RobotMock
from Logic.ReferentialConverter import ReferentialConverter
import sys
sys.path.append("/Mechanical")


with open("../../Commun/config.json") as json_data_file:
    config = json.load(json_data_file)
socketIO = SocketIO(config['url'], int(config['port']))
orderReceiver = OrderReceiver()

def needNewCoordinates(*args):
    orderReceiver.handleCurrentState(args)
    print(orderReceiver.state.__class__)
    socketIO.emit(orderReceiver.state.sendingSignal)

def sendInfo():
    botInfo = orderReceiver.getCurrentRobotInformation()
    socketIO.emit('sendingInfo', botInfo)

def startRound(*args):
    orderReceiver.acceptOrders()
    position = (int(args[0]["positionX"]), int(args[0]["positionY"]))
    orientation = int(args[0]["orientation"])

    orderReceiver.initializeBot(position, orientation)
    sendInfo()
    socketIO.emit(orderReceiver.state.sendingSignal)

def endRound():
    orderReceiver.refuseOrders()

socketIO.emit('sendBotClientStatus','Connected')
socketIO.on('needUpdatedInfo', sendInfo)

socketIO.on('sendNextCoordinates', needNewCoordinates)
socketIO.on('startSignalRobot', startRound)
socketIO.on('sendEndSignal', endRound)


socketIO.wait()




