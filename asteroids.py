import pygame
import math
import random

pygame.init()
pygame.mouse.set_visible(False)
DISPLAY_WIDTH = 1200
DISPLAY_HEIGHT = 900
gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
clock = pygame.time.Clock()

NUM_STARS = 35
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (60, 60, 60)
GRAY = (20, 20, 20)
MAX_SPEED = 20


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
                            [[self.center[0] + 20 * math.cos(math.radians(self.theta)),
                              self.center[1] - 20 * math.sin(math.radians(self.theta))],
                             [self.center[0] + 20 * math.cos(math.radians(self.theta - 130)),
                              self.center[1] - 20 * math.sin(math.radians(self.theta - 130))],
                             [self.center[0] + 5 * math.cos(math.radians(self.theta - 180)),
                              self.center[1] - 5 * math.sin(math.radians(self.theta - 180))],
                             [self.center[0] + 20 * math.cos(math.radians(self.theta + 130)),
                              self.center[1] - 20 * math.sin(math.radians(self.theta + 130))]], 2)

    def slowdown(self):
        hypotenuse = (self.momentum[0] ** 2 + self.momentum[1] ** 2) ** (1 / 2)
        if self.momentum[0] > 0:
            self.momentum[0] -= 0.05 * abs(self.momentum[0] / hypotenuse)
        elif self.momentum[0] < 0:
            self.momentum[0] += 0.05 * abs(self.momentum[0] / hypotenuse)
        if self.momentum[1] > 0:
            self.momentum[1] -= 0.05 * abs(self.momentum[1] / hypotenuse)
        elif self.momentum[1] < 0:
            self.momentum[1] += 0.05 * abs(self.momentum[1] / hypotenuse)

    def speedup(self):
        hypotenuse = (self.momentum[0] ** 2 + self.momentum[1] ** 2) ** 0.5
        if hypotenuse >= MAX_SPEED:
            self.slowdown()
        self.momentum = [self.momentum[0] + 0.2 * math.cos(math.radians(self.theta)),
                         self.momentum[1] + 0.2 * math.sin(math.radians(self.theta))]

    def travel(self):
        if self.thrusters:
            self.speedup()
        else:
            self.slowdown()
        self.draw_rocket()


class Stars:
    def __init__(self, center, momentum, radius):
        self.center = center
        self.momentum = momentum
        self.radius = radius

    def draw_star(self):
        pygame.draw.circle(gameDisplay, LIGHT_GRAY, (int(self.center[0]), int(self.center[1])), self.radius)

    def move_star(self):
        self.momentum = [-0.05 * rocket.momentum[0] * i.radius, -0.05 * rocket.momentum[1] * self.radius]
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


rocket = Rocket([DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2], 90, [0, 0])
stars = []
for i in range(NUM_STARS):
    stars.append(Stars([random.randint(-50, DISPLAY_WIDTH + 50),
                        random.randint(-50, DISPLAY_HEIGHT + 50)],
                       [0, 0],
                       random.randint(1, 5)))

game_exit = False
while not game_exit:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_exit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                rocket.thrusters = True
            elif event.key == pygame.K_LEFT:
                rocket.delta_theta += 6
            elif event.key == pygame.K_RIGHT:
                rocket.delta_theta -= 6
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                rocket.thrusters = False
            elif event.key == pygame.K_LEFT:
                rocket.delta_theta -= 6
            elif event.key == pygame.K_RIGHT:
                rocket.delta_theta += 6

    gameDisplay.fill(GRAY)
    for i in stars:
        i.move_star()
    rocket.travel()
    pygame.display.update()
    clock.tick(50)
quit()
