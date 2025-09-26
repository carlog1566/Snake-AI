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

# GRID FOR AESTHETIC PURPOSES
def drawGrid():
    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
            grid_rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, 'gray9', grid_rect, 1)

# GAMEPLAY LOOP
while True:
    for event in pygame.event.get():
        # QUIT EVENT
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill('Black')
    drawGrid()
    
    pygame.display.update()
    clock.tick(10)