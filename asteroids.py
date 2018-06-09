import pygame
import math

pygame.init()
pygame.mouse.set_visible(False)
DISPLAY_WIDTH = 1200
DISPLAY_HEIGHT = 900
gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (20, 20, 20)
MAX_SPEED = 20


def drawRocket(center, theta, momentum):
    pygame.draw.polygon(gameDisplay,
            WHITE,
            [[center[0] + 20 * math.cos(math.radians(theta)), center[1] - 20 * math.sin(math.radians(theta))],
                [center[0] + 20 * math.cos(math.radians(theta - 130)), center[1] - 20 * math.sin(math.radians(theta - 130))],
                [center[0] + 5 * math.cos(math.radians(theta - 180)), center[1] - 5 * math.sin(math.radians(theta - 180))],
                [center[0] + 20 * math.cos(math.radians(theta + 130)), center[1] - 20 * math.sin(math.radians(theta  + 130))]], 2)


def slowdown(momentum):
    hypotenuse = (momentum[0]**2 + momentum[1]**2)**(1 / 2)
    if momentum[0] > 0:
        momentum[0] -= 0.05 * abs(momentum[0] / hypotenuse)
    elif momentum[0] < 0:
        momentum[0] += 0.05 * abs(momentum[0] / hypotenuse)
    if momentum[1] > 0:
        momentum[1] -= 0.05 * abs(momentum[1] / hypotenuse)
    elif momentum[1] < 0:
        momentum[1] += 0.05 * abs(momentum[1] / hypotenuse)
    return momentum

def speedup(momentum, theta):
    hypotenuse = (momentum[0]**2 + momentum[1]**2)**0.5
    if hypotenuse >= MAX_SPEED: 
        momentum = slowdown(momentum)
    return [momentum[0] + 0.2 * math.cos(math.radians(theta)), momentum[1] + 0.2 * math.sin(math.radians(theta))]


center = [DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2]
game_exit = False
thrusters = False
theta = 90
delta_theta = 0
momentum = [0, 0]
while not game_exit:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_exit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                thrusters = True
            elif event.key == pygame.K_LEFT:
                delta_theta += 6
            elif event.key == pygame.K_RIGHT:
                delta_theta -= 6
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                thrusters = False
            elif event.key == pygame.K_LEFT:
                delta_theta -= 6
            elif event.key == pygame.K_RIGHT:
                delta_theta += 6


    theta = (theta + delta_theta) % 360
    if thrusters:
        momentum = speedup(momentum, theta)
    else:
        momentum = slowdown(momentum)

    gameDisplay.fill(GRAY)
    center = [(center[0] + momentum[0]) % DISPLAY_WIDTH, (center[1] - momentum[1]) % DISPLAY_HEIGHT]
    drawRocket(center, theta, momentum)
    pygame.display.update()
    clock.tick(50)
quit()
