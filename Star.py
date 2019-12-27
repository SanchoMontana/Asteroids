import pygame
from Rocket import rocket
import random
from constants import *


# Controls the star animations.
class Star:
    def __init__(self, center, momentum, radius):
        self.center = center
        self.momentum = momentum
        self.radius = radius

    def draw_star(self):
        pygame.draw.circle(gameDisplay, LIGHT_GRAY, (int(self.center[0]), int(self.center[1])), self.radius)

    # The speed of the stars is opposite of the direction of the rocket, and proportionate to its radius.
    def move_star(self):
        self.momentum = [-0.05 * rocket.momentum[0] * self.radius, -0.05 * rocket.momentum[1] * self.radius]
        if self.center[0] < -50:
            self.center[0] = DISPLAY_WIDTH + 50
            self.radius = random.randint(1, 5)
        elif self.center[0] > DISPLAY_WIDTH + 50:
            self.center[0] = -50
            self.radius = random.randint(1, 5)
        if self.center[1] < -50:
            self.center[1] = DISPLAY_HEIGHT + 50
            self.radius = random.randint(1, 5)
        elif self.center[1] > DISPLAY_HEIGHT + 50:
            self.center[1] = -50
            self.radius = random.randint(1, 5)
        self.center = [self.center[0] + self.momentum[0], self.center[1] - self.momentum[1]]
        self.draw_star()
