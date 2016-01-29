import json
from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory

class BaseSocket(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        obj = json.loads(payload.decode('utf8'))
        if 'BotStatus' in obj:
            print("Bot connected")

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    factory = WebSocketServerFactory(u"ws://192.168.0.102:9000", debug=False)
    factory.protocol = BaseSocket
    # factory.setProtocolOptions(maxConnections=2)

    reactor.listenTCP(9000, factory)
    reactor.run()