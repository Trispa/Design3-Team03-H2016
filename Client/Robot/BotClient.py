import json
import sys
from socketIO_client import SocketIO
from Logic.OrderReceiver import OrderReceiver
from Logic.WheelManager import WheelManager
from Logic.RobotMock import RobotMock
from Mechanical.MoteurRoue import MoteurRoue
import os
import Shared.Utils as Utils

c = os.path.dirname(__file__)
configPath = os.path.join(c, "..", "..", "Shared", "config.json")

with open(configPath) as json_data_file:
    config = json.load(json_data_file)
socketIO = SocketIO(config['url'], int(config['port']))
orderReceiver = OrderReceiver(RobotMock())

def needNewCoordinates(*args):
    print("heading toward next coordinates")
    orderReceiver.handleCurrentState(args[0])
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
socketIO.on('sendNextCoordinates', needNewCoordinates)
socketIO.on('startSignalRobot', startRound)
socketIO.on('sendEndSignal', endRound)
Utils.setInterval(sendInfo, 5)


socketIO.wait()




