import socket

import pygame
from background import Background
from game_modules import GameModules


class Client:
    PORT = 2620
    SERVER = '25.93.237.255'
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ADDRESS = (SERVER, PORT)
    HEADER = 64
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = "!disconnect"
    CONNECTED = False

    def __init__(self):
        GameModules()

    def run(self):
        app_alive = True

        while app_alive:
            game_modules = GameModules()
            app_alive = game_modules.main_menu(self.screen, self.background)
            if app_alive:
                score = game_modules.game(self.screen, self.background)
                if score == -1:
                    app_alive = False
                else:
                    app_alive = game_modules.scoreboard(self.screen, self.background, score)

        pygame.quit()


if __name__ == '__main__':
    Client()
