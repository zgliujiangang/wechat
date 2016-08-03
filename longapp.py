# coding: utf-8
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template, abort
import json

import message


msgsrv = message.MessageServer()


# tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder="templates")


@app.route('/')
def index():
    return render_template('message.html')


@app.route('/message/')
def message():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        msgsrv.observers.append(ws)
        while True:
            if ws:
                message = ws.receive()
                if message:
                    message = message.split("&")
                    message = {item.split("=")[0]: item.split("=")[1] for item in message}
                    message = json.dumps(message)
                    msgsrv.add_message("%s" % message)
            else:
                abort(404)
    return "Connected!"


if __name__ == '__main__':
    http_server = WSGIServer(('192.168.1.137', 5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()