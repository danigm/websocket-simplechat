# coding: utf-8
import json
import pyirc


class IRC(pyirc.IRC):
    def msg(self, nick, msg):
        self.w.send(json.dumps({'output': msg, 'who': nick}))


def handle_websocket(ws):
    irc = None
    while True:
        message = ws.receive()
        if message is None:
            if irc:
                irc.disconnect()
            break
        else:
            message = json.loads(message)

            if 'host' in message:
                host = message['host']
                nick = message['nick']
                port = int(message['port'])
                channel = message['channel']
                irc = IRC(nick)
                irc.connect(host, port, channel)
                irc.w = ws

                irc.w.send(json.dumps({'output': 'CONNECTED!', 'who': 'SERVER'}))
            elif irc and 'msg' in message:
                irc.send(message['msg'])
                irc.w.send(json.dumps({'output': message['msg'], 'who': irc.nick}))
