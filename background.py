import pygame
import random


class Background:

    def __init__(self):
        self.height = pygame.display.Info().current_h
        self.width = pygame.display.Info().current_w

        self.mothership = pygame.image.load("icons/yomommafatter.png")

        self.font = pygame.font.Font('icons/rainyhearts.ttf', 32)
        self.textX = 10
        self.textY = 10

        self.star_field_slow = []
        self.star_field_medium = []
        self.star_field_fast = []

        for slow_stars in range(50):
            star_loc_x = random.randrange(0, self.width)
            star_loc_y = random.randrange(0, self.height)
            self.star_field_slow.append([star_loc_x, star_loc_y])

        for medium_stars in range(35):
            star_loc_x = random.randrange(0, self.width)
            star_loc_y = random.randrange(0, self.height)
            self.star_field_medium.append([star_loc_x, star_loc_y])

        for fast_stars in range(15):
            star_loc_x = random.randrange(0, self.width)
            star_loc_y = random.randrange(0, self.height)
            self.star_field_fast.append([star_loc_x, star_loc_y])
            self.LIGHTGREY = (192, 192, 192)
            self.DARKGREY = (128, 128, 128)
            self.BLACK = (0, 0, 0)
            self.YELLOW = (255, 255, 0)

    def paint_background(self, screen):
        screen.fill(self.BLACK)
        for star in self.star_field_slow:
            star[1] += 1
            if star[1] > self.height:
                star[0] = random.randrange(0, self.width)
                star[1] = random.randrange(-20, -5)
            pygame.draw.circle(screen, self.DARKGREY, star, 3)

        for star in self.star_field_medium:
            star[1] += 4
            if star[1] > self.height:
                star[0] = random.randrange(0, self.width)
                star[1] = random.randrange(-20, -5)
            pygame.draw.circle(screen, self.LIGHTGREY, star, 2)

        for star in self.star_field_fast:
            star[1] += 8
            if star[1] > self.height:
                star[0] = random.randrange(0, self.width)
                star[1] = random.randrange(-20, -5)
            pygame.draw.circle(screen, self.YELLOW, star, 1)

    def paintGame(self, screen):
        screen.blit(self.mothership, (0, 894))

