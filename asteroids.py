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

def drawRocket(center, direction, acceleration):
#    pygame.draw.polygon(gameDisplay,
#            white,
#            [[center[0], center[1] - 15], 
#                [center[0] - 10, center[1] + 15], 
#                [center[0] + 10, center[1] + 15]],
#            1)
    pygame.draw.polygon(gameDisplay,
            white,
            [[center[0] + 15 * math.cos(math.radians(direction)), center[1] - 15 * math.sin(math.radians(direction))],
                [center[0] - 10 * math.cos(math.radians(direction)), center[1] + 15 * math.sin(math.radians(direction))],
                [center[0] + 10 * math.cos(math.radians(direction)), center[1] + 15 * math.sin(math.radians(direction))]],
            1)
    
    

game_exit = False
direction = 90
dir_change = 0
while not game_exit:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_exit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                dir_change = -1
            elif event.key == pygame.K_d:
                dir_change = 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                dir_change += 1
            elif event.key == pygame.K_d:
                dir_change -= 1

    direction = (direction + dir_change) % 360
    gameDisplay.fill(gray)
    drawRocket(center, direction, 3)
    pygame.display.update()
quit()
