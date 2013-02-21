#!/usr/bin/env python2

from twisted.internet import protocol, reactor
from txws import WebSocketFactory


clientnames = {}
clients = []


class Echo(protocol.Protocol):
    def dataReceived(self, data):
        if data.startswith("username:"):
            clientnames[self] = data.split(":")[1]
            return

        for client in clients:
            client.transport.write(clientnames.get(self, '') + ": " + data)

    def connectionMade(self):
        global clients
        clients.append(self)

    def connectionLost(self, reason):
        global clients
        clientnames.pop(self, '')
        clients.remove(self)

class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Echo()

reactor.listenTCP(8080, WebSocketFactory(EchoFactory()))
reactor.run()
