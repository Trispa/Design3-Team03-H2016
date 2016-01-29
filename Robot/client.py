import json

from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory


class MyClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        obj = {"BotStatus" : "Connected"}
        payload = json.dumps(obj, ensure_ascii = False).encode('utf8')
        self.sendMessage(payload)

    # def onOpen(self):
    #     print("WebSocket connection open.")
    #
    #     def hello():
    #         obj = {"key" : "value"}
    #         payload = json.dumps(obj, ensure_ascii = False).encode('utf8')
    #         self.sendMessage(payload)
    #         #self.factory.reactor.callLater(1, hello)
    #
    #     # start sending messages every second ..
    #     hello()

    # def onMessage(self, payload, isBinary):
    #     obj = json.loads(payload.decode('utf8'))
    #     obj["cat"] = "minou"
    #     payload2 = json.dumps(obj, ensure_ascii = False).encode('utf8')
    #     self.sendMessage(payload2)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    factory = WebSocketClientFactory(u"ws://192.168.0.102:9000", debug=False)
    factory.protocol = MyClientProtocol

    reactor.connectTCP("192.168.0.102", 9000, factory)
    reactor.run()