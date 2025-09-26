import pygame
import random
from sys import exit

# DEFINE CONSTANTS
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
PLAYER_START_POS = 200
BLOCK_SIZE = 20

# DEFINE SNAKE POSITION AND STARTING SIZE
snake_position = [PLAYER_START_POS, PLAYER_START_POS]
snake_size = [[200, 200],
              [180, 200],
              [160, 200],
              [140, 200]
              ]

# DEFINE DIRECTION FOR PLAYER INPUT (change_direction used as a buffer so that the computer doesn't freak out when it detects fast inputs)
direction = "RIGHT"
change_direction = direction

# DEFINE APPLE POSITION AND BOOL TO SPAWN APPLE
apple_position = [random.randrange(0, WINDOW_WIDTH, BLOCK_SIZE), random.randrange(0, WINDOW_HEIGHT, BLOCK_SIZE)]
spawn_apple = False

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

        # PLAYER INPUT
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                change_direction = "UP"
            elif event.key == pygame.K_s:
                change_direction = "DOWN"
            elif event.key == pygame.K_a:
                change_direction = "LEFT"
            elif event.key == pygame.K_d:
                change_direction = "RIGHT"

    if game_active:
        # DIRECTION VAR BUFFER
        if change_direction == "UP" and direction != "DOWN":
            direction = "UP"
        if change_direction == "DOWN" and direction != "UP":
            direction = "DOWN"
        if change_direction == "RIGHT" and direction != "LEFT":
            direction = "RIGHT"
        if change_direction == "LEFT" and direction != "RIGHT":
            direction = "LEFT"

        # CHANGE IN SNAKE POSITION BASED ON DIRECTION
        if direction == "UP":
            snake_position[1] -= 20
        if direction == "DOWN":
            snake_position[1] += 20
        if direction == "RIGHT":
            snake_position[0] += 20
        if direction == "LEFT":
            snake_position[0] -= 20

        # DETECTS SNAKE AND APPLE COLLISION AND GROWS THE SNAKE OR WHEN ONE DOESN'T HAPPEN WHERE IT THEN POPS TO KEEP THE SNAKE THE SAME LENGTH
        snake_size.insert(0, list(snake_position))
        if snake_position[0] == apple_position[0] and snake_position[1] == apple_position[1]:
            spawn_apple = False
        else:
            snake_size.pop()

        # USED TO CREATE A NEW POSITION FOR APPLE WITHOUT IT SPAWNING INSIDE THE SNAKE
        if not spawn_apple:
            not_colliding = False
            while not not_colliding:
                for pos in snake_size:
                    apple_position = [random.randrange(0, WINDOW_WIDTH, BLOCK_SIZE), random.randrange(0, WINDOW_HEIGHT, BLOCK_SIZE)]
                    if pos != apple_position:
                        not_colliding = True
                        break

        spawn_apple = True
        screen.fill('Black')
        drawGrid()

        # DRAWS SNAKE IN FRAME
        for pos in snake_size:
            snake_rect = pygame.Rect((pos[0], pos[1]), (BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, 'Green', snake_rect)

        # DRAWS APPLE IN FRAME
        apple_rect = pygame.Rect((apple_position[0], apple_position[1]), (BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(screen, 'Red', apple_rect)
    
    pygame.display.update()
    clock.tick(10)