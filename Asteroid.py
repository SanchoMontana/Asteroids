from constants import *
import random
import math
import pygame.draw
if __name__ == "__main__":
    from asteroids import gameDisplay

asteroids = []


class Asteroids:
    def __init__(self, size, theta, momentum, center=None):
        global asteroids
        if center is None:
            center = []
        self.size = size
        self.new_size = self.size - 1
        self.momentum = momentum
        self.theta = theta
        self.points = []
        self.delta_theta = 0
        self.delta_theta2 = 0
        self.new_momentum = 0
        self.new_momentum2 = 0
        if center:
            self.center = center
        else:
            # Ensures that the starting point of each asteroid is off of the screen,
            # and travels across the screen (for the most part).
            if 0 <= self.theta <= 90:
                if random.getrandbits(1):
                    self.center = [-50, random.randint(0, DISPLAY_HEIGHT / 2)]
                else:
                    self.center = [random.randint(0, DISPLAY_WIDTH / 2), -50]
            elif 90 <= self.theta <= 180:
                if random.getrandbits(1):
                    self.center = [DISPLAY_WIDTH + 50, random.randint(0, DISPLAY_HEIGHT / 2)]
                else:
                    self.center = [random.randint(DISPLAY_WIDTH / 2, DISPLAY_WIDTH), -50]
            elif 180 <= self.theta <= 270:
                if random.getrandbits(1):
                    self.center = [DISPLAY_WIDTH + 50, random.randint(DISPLAY_HEIGHT / 2, DISPLAY_HEIGHT)]
                else:
                    self.center = [random.randint(DISPLAY_WIDTH / 2, DISPLAY_WIDTH), DISPLAY_HEIGHT + 50]
            elif 270 <= self.theta <= 360:
                if random.getrandbits(1):
                    self.center = [-50, random.randint(DISPLAY_HEIGHT / 2, DISPLAY_HEIGHT)]
                else:
                    self.center = [random.randint(0, DISPLAY_WIDTH / 2), DISPLAY_HEIGHT + 50]

        # Randomizes the shape of each asteroid.
        for point in range(10):
            variance = random.randint(self.size * -4, self.size * 4)
            self.points.append([self.center[0] + (self.size * 17 + variance) * math.cos(math.radians(36 * point)),
                                self.center[1] + (self.size * 17 + variance) * math.sin(math.radians(36 * point))])

    # Movement of the asteroids.
    def travel(self):
        self.center[0] += self.momentum * math.cos(math.radians(self.theta))
        self.center[1] += self.momentum * math.sin(math.radians(self.theta))
        for point in self.points:
            point[0] += self.momentum * math.cos(math.radians(self.theta))
            point[1] += self.momentum * math.sin(math.radians(self.theta))
        pygame.draw.polygon(gameDisplay, WHITE, self.points, 2)
        # Memory saver.
        if not (-50 <= self.center[0] <= DISPLAY_WIDTH + 50) \
                or not (-50 <= self.center[1] <= DISPLAY_HEIGHT + 50):
            asteroids.remove(self)
            del self

    def split(self):
        if self.size > 1:
            for i in range(2):
                self.delta_theta = random.randint(0, 90)
                self.delta_theta2 = -1 * self.delta_theta + random.randint(-15, 15)
                self.new_momentum = random.randint(2, 8)
                self.new_momentum2 = random.randint(4, 6)
                asteroids.append(Asteroids(self.new_size, (self.theta + random.randint(0, 90)) % 360, random.randint(2, 8), self.center))
        asteroids.remove(self)
        del self
