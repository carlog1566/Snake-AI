import pygame
from sys import exit

# DEFINE CONSTANTS
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
PLAYER_START_POS = 200
BLOCK_SIZE = 20

# PYGAME ESSENTIALS
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()
game_active = True

# GAMEPLAY LOOP
while True:
    for event in pygame.event.get():
        # QUIT EVENT
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.update()
    clock.tick(10)