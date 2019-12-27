from constants import *
import math
import pygame.draw
if __name__ == "__main__":
    from asteroids import gameDisplay


# Contains all of the methods needed to handle rocket movement and rotation.
class Rocket:
    def __init__(self, center, theta, momentum):
        self.center = center
        self.theta = theta
        self.momentum = momentum
        self.thrusters = False
        self.delta_theta = 0

    def draw_rocket(self):
        self.center = [(self.center[0] + self.momentum[0]) % DISPLAY_WIDTH,
                       (self.center[1] - self.momentum[1]) % DISPLAY_HEIGHT]
        self.theta = (self.theta + self.delta_theta) % 360
        pygame.draw.polygon(gameDisplay,
                            WHITE,
                            [[self.center[0] + ROCKET_SIZE * math.cos(math.radians(self.theta)),
                              self.center[1] - ROCKET_SIZE * math.sin(math.radians(self.theta))],
                             [self.center[0] + ROCKET_SIZE * math.cos(math.radians(self.theta - 130)),
                              self.center[1] - ROCKET_SIZE * math.sin(math.radians(self.theta - 130))],
                             [self.center[0] + ROCKET_SIZE / 4 * math.cos(math.radians(self.theta - 180)),
                              self.center[1] - ROCKET_SIZE / 4 * math.sin(math.radians(self.theta - 180))],
                             [self.center[0] + ROCKET_SIZE * math.cos(math.radians(self.theta + 130)),
                              self.center[1] - ROCKET_SIZE * math.sin(math.radians(self.theta + 130))]], 2)

    # Slows the rocket when thrusters are not being used.
    def slowdown(self):
        hypotenuse = (self.momentum[0] ** 2 + self.momentum[1] ** 2) ** (1 / 2)
        if self.momentum[0] > 0:
            self.momentum[0] -= DECELERATION_RATE * abs(self.momentum[0] / hypotenuse)
        elif self.momentum[0] < 0:
            self.momentum[0] += DECELERATION_RATE * abs(self.momentum[0] / hypotenuse)
        if self.momentum[1] > 0:
            self.momentum[1] -= DECELERATION_RATE * abs(self.momentum[1] / hypotenuse)
        elif self.momentum[1] < 0:
            self.momentum[1] += DECELERATION_RATE * abs(self.momentum[1] / hypotenuse)
        if hypotenuse < 0.1:
            self.momentum = [0, 0]

    # Speeds up the rocket when thrusters are in use.
    def speedup(self):
        hypotenuse = (self.momentum[0] ** 2 + self.momentum[1] ** 2) ** 0.5
        if hypotenuse >= MAX_SPEED:
            self.slowdown()
            return
        self.momentum = [self.momentum[0] + ACCELERATION_RATE * math.cos(math.radians(self.theta)),
                         self.momentum[1] + ACCELERATION_RATE * math.sin(math.radians(self.theta))]

    # Called in the main loop to prevent the need for a few more "if else" statements.
    def travel(self):
        if self.thrusters:
            self.speedup()
        else:
            self.slowdown()
        self.draw_rocket()


rocket = Rocket([DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2], 90, [0, 0])  # Instantiates a Rocket object.
