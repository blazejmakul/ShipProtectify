import pygame
import random


class Meteor:
    def __init__(self):
        meteor_types = ("icons/one32x.png", "icons/one64x.png", "icons/one128x.png", "icons/two128x.png", "icons"
                                                                                                          "/two64x.png")
        self.meteor_type = meteor_types[random.randrange(0, len(meteor_types) - 1)]
        self.meteor = pygame.image.load(self.meteor_type)
        self.X = random.randrange(0, 400)
        self.Y = 1
        self.onMap = True

    def paint(self, screen):
        screen.blit(self.meteor, (self.X, self.Y))

    def move(self):
        self.Y += 3
        if self.Y > 840:
            self.onMap = False
