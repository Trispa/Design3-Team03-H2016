import json

from Logic.OrderReceiver import OrderReceiver
from socketIO_client import SocketIO
from Logic.RobotMock import RobotMock
from Logic.ReferentialConverter import ReferentialConverter
import sys
sys.path.append("/Mechanical")
import threading

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

with open("../../Commun/config.json") as json_data_file:
    config = json.load(json_data_file)
socketIO = SocketIO(config['url'], int(config['port']))
orderReceiver = OrderReceiver()

def needNewCoordinates(*args):
    print("heading toward next coordinates")
    orderReceiver.handleCurrentState(args)
    print(orderReceiver.state.__class__)
    socketIO.emit(orderReceiver.state.sendingSignal)

def sendInfo():
    print("sending bot information to base")
    botInfo = orderReceiver.getCurrentRobotInformation()
    socketIO.emit('sendingInfo', botInfo)

def startRound(*args):
    print("start round")
    orderReceiver.acceptOrders()
    position = (int(args[0]["positionX"]), int(args[0]["positionY"]))
    orientation = int(args[0]["orientation"])
    orderReceiver.initializeBot(position, orientation)
    sendInfo()
    socketIO.emit(orderReceiver.state.sendingSignal)

def endRound():
    print("end round")
    orderReceiver.refuseOrders()

socketIO.emit('sendBotClientStatus','Connected')
socketIO.on('needUpdatedInfo', sendInfo)

socketIO.on('sendNextCoordinates', needNewCoordinates)
socketIO.on('startSignalRobot', startRound)
socketIO.on('sendEndSignal', endRound)
set_interval(sendInfo, 5)


socketIO.wait()




