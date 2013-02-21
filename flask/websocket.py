# coding: utf-8
import json
import datetime

sockets = []

def handle_websocket(ws):
    sockets.append(ws)
    while True:
        message = ws.receive()
        if message is None:
            sockets.remove(ws)
            break
        else:
            message = json.loads(message)
            print "MESSAGE RECEIVED", message
            date = str(datetime.datetime.now())

            for w in sockets:
                w.send(json.dumps({'output': message['msg'], 'date': date}))
