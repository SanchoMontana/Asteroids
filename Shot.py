from constants import *
import math
import pygame.draw
import random
if __name__ == "__main__":
    from asteroids import gameDisplay


# Allows the user to shoot lasers.
class Shot:
    def __init__(self, center, theta):
        self.theta = theta + random.randint(-2, 2)  # Bullet RNG
        self.center = [center[0] + ROCKET_SIZE / 2 * math.cos(math.radians(self.theta)),
                       center[1] - ROCKET_SIZE / 2 * math.sin(math.radians(self.theta))]
        self.start = []
        self.end = []
        self.life = 0

        # Movement of the lasers (these wrap around the playable area).

    def travel(self):
        self.life += 1
        self.center = [(self.center[0] + SHOT_SPEED * math.cos(math.radians(self.theta))) % DISPLAY_WIDTH,
                       (self.center[1] - SHOT_SPEED * math.sin(math.radians(self.theta))) % DISPLAY_HEIGHT]
        self.start = [self.center[0] - SHOT_LENGTH / 2 * math.cos(math.radians(self.theta)),
                      self.center[1] + SHOT_LENGTH / 2 * math.sin(math.radians(self.theta))]
        self.end = [self.center[0] + SHOT_LENGTH / 2 * math.cos(math.radians(self.theta)),
                    self.center[1] - SHOT_LENGTH / 2 * math.sin(math.radians(self.theta))]
        pygame.draw.line(gameDisplay,
                         WHITE,
                         self.start, self.end, 4)
