import pygame


class Player:
    def __init__(self, pid, color):
        self.X = 100
        self.Y = 820
        self.change = 0
        self.score = 0
        self.PID = pid
        if color == "red":
            self.playerIcon = pygame.image.load("icons/red64x.png")
        elif color == "green":
            self.playerIcon = pygame.image.load("icons/green64x.png")
        elif color == "blue":
            self.playerIcon = pygame.image.load("icons/blue64x.png")

    def moveLeft(self):
        self.change = -8

    def moveRight(self):
        self.change = 8

    def stopMoving(self):
        self.change = 0

    def move(self):
        self.X += self.change
        if self.X <= 0:
            self.X = 0
        elif self.X >= 450:
            self.X = 450

    def paint(self, screen):
        screen.blit(self.playerIcon, (self.X, self.Y))

    def addPoint(self):
        self.score += 1
