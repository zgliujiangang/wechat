# message.py
from geventwebsocket import WebSocketError


class MessageServer(object):

    def __init__(self):
        self.observers = []

    def add_message(self, msg):
        for ws in self.observers:
            try:
                ws.send(msg)
            except WebSocketError:
                self.observers.pop(self.observers.index(ws))
                print ws, 'is closed'
                continue