from constants import *
import time
import pygame
import random
import Rocket
import Star
import Shot
import Asteroid


# Iterated through all of the shots and all of the asteroids and detects if there is a collision (roughly).
def test_collision(asteroid_list):
    for shot in shots:
        for asteroid in asteroid_list:
            if asteroid.center[0] - asteroid.size * 17 < shot.center[0] < asteroid.center[0] + asteroid.size * 17 \
                    and asteroid.center[1] - asteroid.size * 17 < shot.center[1] < asteroid.center[1] + asteroid.size * 17:
                shots.remove(shot)
                asteroid.split()
                break


stars = []  # This empty list will be populated with Star objects.
shots = []  # This empty list will be populated with Shot objects.

for i in range(NUM_STARS):  # Loop that will populate the stars array with NUM_STARS stars.
    stars.append(Star.Star([random.randint(-50, DISPLAY_WIDTH + 50),
                            random.randint(-50, DISPLAY_HEIGHT + 50)],
                           [0, 0],
                           random.randint(1, 5)))
no_repeat = 0  # TEMPORARY - This is used to create one asteroid every three seconds.

# Main loop:
game_exit = False
while not game_exit:
    # Event handling.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_exit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                Rocket.rocket.thrusters = True
            elif event.key == pygame.K_LEFT:
                Rocket.rocket.delta_theta += 6
            elif event.key == pygame.K_RIGHT:
                Rocket.rocket.delta_theta -= 6
            elif event.key == pygame.K_SPACE:
                shots.append(Shot.Shot(Rocket.rocket.center, Rocket.rocket.theta))
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                Rocket.rocket.thrusters = False
            elif event.key == pygame.K_LEFT:
                Rocket.rocket.delta_theta -= 6
            elif event.key == pygame.K_RIGHT:
                Rocket.rocket.delta_theta += 6

    # gameDisplay updates.
    gameDisplay.fill(GRAY)

    # Need to replace, so that difficulty will slowly increase over time.
    if int(time.time()) % 7 == 0 and int(time.time()) != no_repeat:
        Asteroid.asteroids.append(Asteroid.Asteroids(random.randint(1, 3), random.randint(1, 360), random.randint(MIN_ASTEROID_SPEED, MAX_ASTEROID_SPEED)))
        no_repeat = int(time.time())

    test_collision(Asteroid.asteroids)
    for i in stars:
        i.move_star()
    for i in shots:
        if i.life >= SHOT_LIFE:
            shots.remove(i)
            del i
        else:
            i.travel()
    for i in Asteroid.asteroids:
        i.travel()

    Rocket.rocket.travel()
    pygame.display.update()
    clock.tick(FPS)

# There is no need for pygame.quit().
quit()
