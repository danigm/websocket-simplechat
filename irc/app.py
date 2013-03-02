# coding: utf-8
# based on http://www.socketubs.net/2012/10/28/Websocket_with_flask_and_gevent/

import os

from flask import Flask
from flask import render_template
from websocket import handle_websocket

PORT = 5000
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.debug = True

def my_app(environ, start_response):
    path = environ["PATH_INFO"]
    if path == "/":
        return app(environ, start_response)
    elif path == "/websocket":
        handle_websocket(environ["wsgi.websocket"])
    else:
        return app(environ, start_response)

@app.route("/")
def hello():
    return render_template('index.html', port=PORT)


if __name__ == '__main__':
    from gevent.pywsgi import WSGIServer
    from geventwebsocket.handler import WebSocketHandler

    http_server = WSGIServer(('', PORT), my_app, handler_class=WebSocketHandler)
    http_server.serve_forever()
