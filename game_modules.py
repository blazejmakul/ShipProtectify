import threading
import time

import pygame
from bullet import Bullet
from meteor import Meteor
from player import Player
import menu_screens
import socket
from background import Background


class GameModules:
    connection = 0

    def __init__(self):
        self.players = []
        self.readyPlayers = 0
        self.ready = False
        self.client = None
        self.CONNECTED = False
        self.DISCONNECT_MESSAGE = "!disconnect"
        self.FORMAT = 'utf-8'
        self.HEADER = 64
        self.ClientID = 0
        self.menu = True
        pygame.init()
        self.background = Background()
        self.screen = pygame.display.set_mode([512, 1024])
        pygame.display.set_icon(pygame.image.load("icons/red32x.png"))
        self.game_alive = False
        self.fail = False
        self.connected_clients = 0
        self.alive = True
        self.wait = False
        self.sb = False
        self.game_over = pygame.mixer.Sound("icons/sounds/game_over.wav")
        self.button_click = pygame.mixer.Sound("icons/sounds/button.mp3")
        self.laser = pygame.mixer.Sound("icons/sounds/laser.wav")
        pygame.mixer.music.load("icons/sounds/music.mp3")
        while self.alive:
            self.main_menu(self.screen)
            self.game(self.screen, self.background)

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        PORT = 2620
        SERVER = '25.97.113.99'
        ADDRESS = (SERVER, PORT)

        print("Connecting")
        try:
            self.client.connect(ADDRESS)
        except ConnectionRefusedError:
            self.connection = -1
            return
        print("Connected")
        length = int(self.client.recv(self.HEADER).decode(self.FORMAT))
        self.ClientID = int(self.client.recv(length).decode(self.FORMAT))
        self.connection = 1
        thread = threading.Thread(target=self.receive)
        thread.start()

    def send(self, msg):
        message = msg.encode(self.FORMAT)
        print(f"SEND: {msg}")
        send_len = str(len(message)).encode(self.FORMAT)
        send_len += b' ' * (self.HEADER - len(send_len))
        self.client.send(send_len)
        self.client.send(message)

    def receive(self):
        while self.connection == 1:
            try:
                msg_len = int(self.client.recv(self.HEADER).decode(self.FORMAT))
                msg = str(self.client.recv(msg_len).decode(self.FORMAT)).split(":")
                print(f"RECEIVE: {msg}")
                if msg[0] == self.DISCONNECT_MESSAGE:
                    self.connection = 0
                    self.client = None
                elif msg[0] == "START":
                    self.menu = False
                    self.game_alive = True
                elif msg[0] == "CON":  # CON:PID
                    player = [int(msg[1]), 0]
                    if player not in self.players:
                        self.connected_clients += 1
                        self.players.append([int(msg[1]), 0])
                    print(self.players)
                elif msg[0] == "DCON":  # DCON:PID
                    self.connected_clients -= 1
                    for player in self.players:
                        if int(msg[1]) == player[0]:
                            self.players.remove(player)
                            break
                    print(self.players)
                elif msg[0] == "SC":  # SC:PID:QTY
                    for player in self.players:
                        if player[0] == int(msg[1]):
                            player[1] = int(msg[2])
                elif msg[0] == "RD":  # RD:QT
                    self.readyPlayers = int(msg[1])
                elif msg[0] == "STOP":
                    self.wait = False
            except ConnectionResetError:
                self.connection = 0
                self.connected_clients = 0
                self.players.clear()
                self.ready = 0
                self.sb = False
                self.menu = True
                return
            except AttributeError:
                self.connection = 0
                return
            except ValueError:
                continue
            except IndexError:
                continue

    def main_menu(self, screen):
        clock = pygame.time.Clock()

        while self.menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.connection == 1:
                        self.send(self.DISCONNECT_MESSAGE)
                        self.client = None
                    pygame.quit()
                    self.alive = False
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] in range(315, 315 + 64) and mouse[1] in range(500, 500 + 64):
                        self.button_click.play()
                        if self.connection == 1:
                            if not self.ready:
                                self.ready = True
                                self.send(f"{self.ClientID}:READY")
                            else:
                                self.ready = False
                                self.send(f"{self.ClientID}:NOT READY")
                    elif mouse[0] in range(120, 120 + 64) and mouse[1] in range(500, 500 + 64):
                        if self.connection == 0:
                            self.button_click.play()
                            self.connection = 2
                            thread = threading.Thread(target=self.connect)
                            thread.start()
            self.background.paint_background(screen)
            menu_screens.paint_main_menu(screen, self.connection, self.ready)
            font = pygame.font.Font('icons/rainyhearts.ttf', 32)
            screen.blit(font.render(f"Connected: {self.connected_clients} / Ready: {self.readyPlayers}", True, (255, 255, 255)), (1, 1))
            pygame.display.update()
            clock.tick(60)
        return True

    def game(self, screen, background):
        if self.ClientID == 1:
            color = "red"
            rgb = (255, 0, 0)
        elif self.ClientID == 2:
            color = "green"
            rgb = (0, 255, 0)
        else:
            color = "blue"
            rgb = (0, 0, 255)
        player = Player(self.ClientID, color)
        bullets = []
        cooldown = 0
        clock = pygame.time.Clock()
        meteors = [Meteor(), Meteor()]

        font = pygame.font.Font('icons/rainyhearts.ttf', 160)
        for i in range(3, 0, -1):
            countDown = font.render(str(i), True, (255, 0, 0))
            screen.fill((0, 0, 0))
            screen.blit(countDown, (230, 400))
            print(i)
            pygame.display.update()
            time.sleep(1)

        start_time = pygame.time.get_ticks()
        for x in self.players:
            x[1] = 0
        self.send(f"P:{0}")
        added = False

        pygame.mixer.music.play()
        while self.game_alive:
            passed_time = pygame.time.get_ticks() - start_time
            timer_value = int(60 - (passed_time / 1000))
            if timer_value <= 0:
                pygame.mixer.music.stop()
                self.game_over.play()
                self.game_alive = False
                self.send(f"{self.ClientID}:NOT READY")
                self.ready = False
                self.sb = True
                self.scoreboard(screen, background)
                return
            if (timer_value % 10) == 0:
                if not added:
                    meteors.append(Meteor())
                    added = True
            else:
                if added:
                    added = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_alive = False
                    self.send(self.DISCONNECT_MESSAGE)
                    self.connection = 0
                    self.client = None
                    pygame.quit()
                    self.alive = False
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        player.moveRight()
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        player.moveLeft()
                    if event.key == pygame.K_SPACE:
                        if cooldown == 0:
                            bullets.append(Bullet(player.X + 32, player.Y - 10))
                            self.laser.play()
                            cooldown = 30
                    if event.key == pygame.K_ESCAPE:
                        return -1
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                        player.stopMoving()

            player.move()
            background.paint_background(screen)
            background.paintGame(screen)
            for bullet in bullets:
                bullet.move()
                if not bullet.onMap:
                    bullets.remove(bullet)
                bullet.paint(screen)
            player.paint(screen)
            for meteor in meteors:
                meteor.move()
                if not meteor.onMap:
                    pygame.mixer.music.stop()
                    self.game_over.play()
                    self.game_alive = False
                    self.wait = True
                    self.send(f"{self.ClientID}:NOT READY")
                    self.ready = False
                    self.scoreboard(screen, background)
                    return
                meteor.paint(screen)
                for bullet in bullets:
                    if bullet.checkCollision(meteor):
                        player.addPoint()
                        self.send(f"P:{player.score}")
                        bullets.remove(bullet)
                        meteors.remove(meteor)
                        meteors.append(Meteor())
            player.paint(screen)
            font = pygame.font.Font('icons/rainyhearts.ttf', 32)
            for x in self.players:
                if x[0] == 1:
                    rgb = (255, 0, 0)
                elif x[0] == 2:
                    rgb = (0, 255, 0)
                else:
                    rgb = (0, 0, 255)

                if x[0] == self.ClientID:
                    msg = font.render(f"You: {x[1]} pt", True, rgb)
                else:
                    msg = font.render(f"Player: {x[0]}: {x[1]} pt", True, rgb)
                screen.blit(msg, (10, x[0] * 30))
            font = pygame.font.Font('icons/rainyhearts.ttf', 50)
            screen.blit(font.render(f"{timer_value}", True, (255, 255, 255)), (440, 32))
            pygame.display.update()
            if cooldown > 0:
                cooldown -= 1
            clock.tick(60)

    def scoreboard(self, screen, background):
        clock = pygame.time.Clock()

        while self.wait and self.sb:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.send(self.DISCONNECT_MESSAGE)
                    pygame.quit()
                    self.alive = False
                    quit()
            background.paint_background(screen)
            font = pygame.font.Font('icons/rainyhearts.ttf', 32)
            for x in self.players:
                if x[0] == 1:
                    rgb = (255, 0, 0)
                elif x[0] == 2:
                    rgb = (0, 255, 0)
                else:
                    rgb = (0, 0, 255)

                if x[0] == self.ClientID:
                    msg = font.render(f"You: {x[1]} pt", True, rgb)
                else:
                    msg = font.render(f"Player: {x[0]}: {x[1]} pt", True, rgb)
                screen.blit(msg, (10, x[0] * 30))
            font = pygame.font.Font('icons/rainyhearts.ttf', 64)
            screen.blit(font.render("Waiting for others...", True, (255, 255, 255)), (40, 400))
            pygame.display.update()
            clock.tick(60)

        self.sb = True
        while self.sb:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.send(self.DISCONNECT_MESSAGE)
                    self.alive = False
                    pygame.quit()
                    self.alive = False
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.game_alive = False
                        self.menu = True
                        return
            background.paint_background(screen)
            sorted_players = sorted(self.players, key=lambda y: y[1], reverse=True)
            font = pygame.font.Font('icons/rainyhearts.ttf', 36)
            if sorted_players[0][0] == self.ClientID:
                msg = f"WINNER: YOU - {sorted_players[0][1]} points!"
            else:
                msg = f"WINNER: Player {sorted_players[0][0]} - {sorted_players[0][1]} points!"
            screen.blit(font.render(msg, True, (255, 255, 0)), (0, 100))

            font = pygame.font.Font('icons/rainyhearts.ttf', 32)
            if len(sorted_players) > 1:
                if sorted_players[1][0] == self.ClientID:
                    msg = f"2nd: YOU - {sorted_players[1][1]} points"
                else:
                    msg = f"2nd: Player {sorted_players[1][0]} - {sorted_players[1][1]} points"
                screen.blit(font.render(msg, True, (255, 255, 255)), (0, 160))
            if len(sorted_players) > 2:
                if sorted_players[2][0] == self.ClientID:
                    msg = f"3rd: YOU - {sorted_players[2][1]} points"
                else:
                    msg = f"3rd: Player {sorted_players[2][0]} - {sorted_players[2][1]} points"
                screen.blit(font.render(msg, True, (255, 255, 255)), (0, 180))
            screen.blit(font.render("Press enter to continue...", True, (255, 255, 255)), (100, 512))
            pygame.display.update()
            clock.tick(60)


if __name__ == '__main__':
    GameModules()
