import socket

import threading
from ClientObject import ClientObject


class Server:

    def __init__(self):
        self.PORT = 2620
        self.SERVER = '0.0.0.0'
        self.ADDRESS = (self.SERVER, self.PORT)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDRESS)
        self.HEADER = 64
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!disconnect"
        self.connected_clients = 0
        self.ready_clients = 0
        self.clientsList = []
        self.game_alive = False

    def handle_client(self, connection, address, clientID, this):
        print(f"[SERVER]  {address} connected")
        ready = False
        while True:
            print(f"{clientID} alive!")
            try:
                msg_len = int(connection.recv(self.HEADER).decode(self.FORMAT))
            except ConnectionResetError:
                print(f"{clientID} closed the connection")
                if ready:
                    self.ready_clients -= 1
                    self.sendToALL(f"RD:{self.ready_clients}")
                self.connected_clients -= 1
                self.clientsList.remove(this)
                self.sendToALL(f"DCON:{clientID}")
                return
            except ValueError:
                print(f"{clientID} closed the connection")
                if ready:
                    self.ready_clients -= 1
                    self.sendToALL(f"RD:{self.ready_clients}")
                self.connected_clients -= 1
                self.clientsList.remove(this)
                self.sendToALL(f"DCON:{clientID}")
                return
            msg = str(connection.recv(msg_len).decode(self.FORMAT))
            print(f"RECEIVED: {msg}")
            if msg == self.DISCONNECT_MESSAGE:
                print(f"{clientID} closed the connection")
                if ready:
                    self.ready_clients -= 1
                    self.sendToALL(f"RD:{self.ready_clients}")
                self.connected_clients -= 1
                self.clientsList.remove(this)
                self.sendToALL(f"DCON:{clientID}")
                connection = None
                address = None
                return
            if len(msg) > 1:
                split_msg = msg.split(":")
                if split_msg[0] == self.DISCONNECT_MESSAGE:
                    self.send(connection, self.DISCONNECT_MESSAGE)
                elif split_msg[1] == "READY":
                    self.ready_clients += 1
                    ready = True
                    self.sendToALL(f"RD:{self.ready_clients}")
                    print(f"{clientID} client is ready")
                    if self.connected_clients == self.ready_clients and self.connected_clients > 1:
                        self.sendToALL("START")
                        self.game_alive = True
                elif split_msg[1] == "NOT READY":
                    self.ready_clients -= 1
                    ready = False
                    if self.game_alive and self.ready_clients == 0:
                        self.sendToALL("STOP")
                        self.game_alive = False
                    print(f"{clientID} client is not ready")
                    self.sendToALL(f"RD:{self.ready_clients}")
                elif split_msg[0] == "P":
                    self.sendToALL(f"SC:{clientID}:{int(split_msg[1])}")

    def start(self):
        self.server.listen()
        while True:
            if self.connected_clients < 3:
                connection, address = self.server.accept()
                self.connected_clients += 1
                current_id = []
                assign_id = 0
                if self.connected_clients > 1:
                    for x in self.clientsList:
                        current_id.append(x.clientID)
                if 1 not in current_id:
                    assign_id = 1
                elif 2 not in current_id:
                    assign_id = 2
                elif 3 not in current_id:
                    assign_id = 3
                self.send(connection, str(assign_id))
                this = ClientObject(assign_id, connection)
                self.clientsList.append(this)
                for x in self.clientsList:
                    self.send(connection, f"CON:{x.clientID}")
                self.sendToALL(f"CON:{assign_id}")
                thread = threading.Thread(target=self.handle_client, args=(connection, address, self.connected_clients, this))
                thread.start()

    def send(self, connection, msg):
        print(f"SEND: {msg}")
        message = msg.encode(self.FORMAT)
        send_len = str(len(message)).encode(self.FORMAT)
        send_len += b' ' * (self.HEADER - len(send_len))
        connection.send(send_len)
        connection.send(message)

    def sendToALL(self, msg):
        for i in self.clientsList:
            self.send(i.connection, msg)

    def userInput(self):
        command = input()
        if command.lower() == "stop":
            self.sendToALL(self.DISCONNECT_MESSAGE)
            exit()


if __name__ == '__main__':
    server = Server()
    thread = threading.Thread(target=server.userInput)
    thread.start()
    server.start()
