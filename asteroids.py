import pygame
import math
import random

pygame.init()
pygame.mouse.set_visible(False)
DISPLAY_WIDTH = 1200
DISPLAY_HEIGHT = 900
gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
clock = pygame.time.Clock()

FPS = 50  # Frames per second.
ROCKET_SIZE = 20  # Pixels from center of the rocket to its front point.
ACCELERATION_RATE = 0.2  # Momentum increase of rocket when thrusters are on.
DECELERATION_RATE = 0.03  # Momentum decrease of rocket when thrusters are off.
SHOT_LENGTH = 20  # Pixels
SHOT_SPEED = 30  # Pixels per Frame
SHOT_LIFE = 20  # Frames
NUM_STARS = 35
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (60, 60, 60)
GRAY = (20, 20, 20)
RED = (255, 0, 0)
MAX_SPEED = 20


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

    # Speeds up the rocket when thrusters are in use.
    def speedup(self):
        hypotenuse = (self.momentum[0] ** 2 + self.momentum[1] ** 2) ** 0.5
        if hypotenuse >= MAX_SPEED:
            self.slowdown()
        self.momentum = [self.momentum[0] + ACCELERATION_RATE * math.cos(math.radians(self.theta)),
                         self.momentum[1] + ACCELERATION_RATE * math.sin(math.radians(self.theta))]

    # Called in the main loop to prevent the need for a few more "if else" statements.
    def travel(self):
        if self.thrusters:
            self.speedup()
        else:
            self.slowdown()
        self.draw_rocket()


# Allows the user to shoot lasers.
class Shot:
    def __init__(self, center, theta):
        self.theta = theta
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


rocket = Rocket([DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2], 90, [0, 0])  # Instantiates a Rocket object.

stars = []  # This empty list will be populated with Star objects.
shots = []  # This empty list will be populated with Shot objects.

for i in range(NUM_STARS):  # Loop that will populate the stars array with NUM_STARS stars.
    stars.append(Star([random.randint(-50, DISPLAY_WIDTH + 50),
                       random.randint(-50, DISPLAY_HEIGHT + 50)],
                      [0, 0],
                      random.randint(1, 5)))

# Main loop:
game_exit = False
while not game_exit:
    # Event handling.
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
            elif event.key == pygame.K_SPACE:
                shots.append(Shot(rocket.center, rocket.theta))
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                rocket.thrusters = False
            elif event.key == pygame.K_LEFT:
                rocket.delta_theta -= 6
            elif event.key == pygame.K_RIGHT:
                rocket.delta_theta += 6

    # gameDisplay updates.
    gameDisplay.fill(GRAY)
    for i in shots:
        if i.life >= SHOT_LIFE:
            shots.remove(i)
            del i
        else:
            i.travel()
    for i in stars:
        i.move_star()
    rocket.travel()
    pygame.display.update()
    clock.tick(FPS)

# There is no need for pygame.quit().
quit()
