#
# Implementing a simple socket tick data CLIENT
# with autobahn & Twisted
#
# The Python Quants GmbH
#
import random
from autobahn.twisted.websocket import WebSocketClientProtocol, \
                                       WebSocketClientFactory

class TickStreamer(WebSocketClientProtocol):
    def onConnect(self, response):
        print('Server connected: {0}'.format(response.peer))

    def onOpen(self):
        global i
        print('WebSocket connection open.')
        def req():
            self.sendMessage(u'request quote'.encode('utf8'))
            # randomize data retrieval times
            self.factory.reactor.callLater(3 * random.random() + 0.2, req)
        req()

    def onMessage(self, payload, isBinary):
        print('new data: {0}'.format(payload.decode('utf8')))

    def onClose(self, wasClean, code, reason):
        print('WebSocket connection closed: {0}'.format(reason))


if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    factory = WebSocketClientFactory(u'ws://127.0.0.1:9000', debug=False)
    factory.protocol = TickStreamer
    reactor.connectTCP('127.0.0.1', 9000, factory)
    reactor.run()
