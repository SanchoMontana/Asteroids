import pygame

DISPLAY_WIDTH = 1200
DISPLAY_HEIGHT = 900
FPS = 50  # Frames per second.
ROCKET_SIZE = 20  # Pixels from center of the rocket to its front point.
ACCELERATION_RATE = 0.5  # Momentum increase of rocket when thrusters are on.
DECELERATION_RATE = 0.5  # Momentum decrease of rocket when thrusters are off.
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
MIN_ASTEROID_SPEED = 1
MAX_ASTEROID_SPEED = 4

pygame.init()
pygame.mouse.set_visible(False)
gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
clock = pygame.time.Clock()