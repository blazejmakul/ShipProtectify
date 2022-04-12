import socket
from meteor import Meteor


class ClientObject:
    def __init__(self, clientID, connection):
        self.clientID = clientID
        self.ready = False
        self.connection = connection
        self.X = 100
        self.Y = 820
        self.score = 0
        self.bullets = []
