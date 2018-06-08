import pygame
import math

pygame.init()
clock = pygame.time.Clock()
white = (255, 255, 255)
black = (0, 0, 0)
gray = (20, 20, 20)
pygame.mouse.set_visible(False)
displayWidth = 800
displayHeight = 600
gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))

pygame.display.update()

center = [displayWidth / 2, displayHeight / 2]

def drawRocket(center, theta, momentum):
    pygame.draw.polygon(gameDisplay,
            white,
            [[center[0] + 20 * math.cos(math.radians(theta)), center[1] - 20 * math.sin(math.radians(theta))],
                [center[0] + 20 * math.cos(math.radians(theta - 130)), center[1] - 20 * math.sin(math.radians(theta - 130))],
                [center[0] + 5 * math.cos(math.radians(theta - 180)), center[1] - 5 * math.sin(math.radians(theta - 180))],
                [center[0] + 20 * math.cos(math.radians(theta + 130)), center[1] - 20 * math.sin(math.radians(theta  + 130))]],
            2)

def slowdown(momentum):
    if momentum[0] > 0:
        momentum[0] -= 0.1
    elif momentum[0] < 0:
        momentum[0] += 0.1
    
    if momentum[1] > 0:
        momentum[1] -= 0.1
    elif momentum[1] < 0:
        momentum[1] += 0.1
    return momentum

def speedup(momentum, theta):
    return [momentum[0] + 0.2 * math.cos(math.radians(theta)), momentum[1] + 0.2 * math.sin(math.radians(theta))]

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

    gameDisplay.fill(gray)
    center = [center[0] + momentum[0], center[1] - momentum[1]]
    drawRocket(center, theta, momentum)
    pygame.display.update()
    clock.tick(50)
quit()
