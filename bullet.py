import pygame
from meteor import Meteor


class Bullet:
    def __init__(self, x, y):
        self.X = x
        self.Y = y
        self.onMap = True
        self.color = (255, 255, 0)

    def move(self):
        self.Y -= 5
        if self.Y <= 0:
            self.onMap = False

    def checkCollision(self, meteor):
        if meteor.onMap:
            if "32" in meteor.meteor_type:
                if self.X in range(meteor.X, meteor.X+30) and self.Y in range(meteor.Y, meteor.Y+30):
                    return True
                else:
                    return False
            if "64" in meteor.meteor_type:
                if self.X in range(meteor.X, meteor.X+60) and self.Y in range(meteor.Y, meteor.Y+60):
                    return True
                else:
                    return False
            if "128" in meteor.meteor_type:
                if self.X in range(meteor.X, meteor.X+120) and self.Y in range(meteor.Y, meteor.Y+120):
                    return True
                else:
                    return False

    def paint(self, screen):
        pygame.draw.circle(screen, self.color, (self.X, self.Y), 5)
