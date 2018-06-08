import pygame
import math

pygame.init()
white = (255, 255, 255)
black = (0, 0, 0)
gray = (20, 20, 20)
pygame.mouse.set_visible(False)
displayWidth = 800
displayHeight = 600
gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))

pygame.display.update()

center = [displayWidth / 2, displayHeight / 2]

def drawRocket(center, theta, acceleration):
#    pygame.draw.polygon(gameDisplay,
#            white,
#            [[center[0], center[1] - 15], 
#                [center[0] - 10, center[1] + 15], 
#                [center[0] + 10, center[1] + 15]],
#            1)
    pygame.draw.polygon(gameDisplay,
            white,
            [[center[0] + 20 * math.cos(math.radians(theta)), center[1] - 20 * math.sin(math.radians(theta))],
                [center[0] + 20 * math.cos(math.radians(theta - 130)), center[1] - 20 * math.sin(math.radians(theta - 130))],
                [center[0] + 5 * math.cos(math.radians(theta - 180)), center[1] - 5 * math.sin(math.radians(theta - 180))],
                [center[0] + 20 * math.cos(math.radians(theta + 130)), center[1] - 20 * math.sin(math.radians(theta  + 130))]],
            2)
    
    

game_exit = False
theta = 90
delta_theta = 0
while not game_exit:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_exit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                delta_theta += 0.5
            elif event.key == pygame.K_RIGHT:
                delta_theta -= 0.5
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                delta_theta -= 0.5
            elif event.key == pygame.K_RIGHT:
                delta_theta += 0.5
    theta = (theta + delta_theta) % 360
    gameDisplay.fill(gray)
    drawRocket(center, theta, 3)
    pygame.display.update()
quit()
