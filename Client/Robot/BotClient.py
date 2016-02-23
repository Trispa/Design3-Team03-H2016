import json

from Logic.OrderReceiver import OrderReceiver
from socketIO_client import SocketIO

with open("../../Shared/config.json") as json_data_file:
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

def startRound():
    orderReceiver.acceptOrders()
    orderReceiver.initializeBot()
    sendInfo()
    socketIO.emit(orderReceiver.state.sendingSignal)

def endRound():
    orderReceiver.refuseOrders()

socketIO.emit('sendingBotClientStatus','Connected')
socketIO.on('needUpdatedInfo', sendInfo)
socketIO.on('sendingNextCoordinates', needNewCoordinates)
socketIO.on('startSignal', startRound)
socketIO.on('sendingEndSignal', endRound)

socketIO.wait()




