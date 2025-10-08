import os
import pygame
import random
from sys import exit
from enum import Enum
from collections import namedtuple

# reset
# reward
# play(action) -> direction
# game iteration
# collision

pygame.init()
font_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'font', 'Pixeltype.ttf')
score_font = pygame.font.Font(font_path, 50)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

WINDOW_HEIGHT = 860
WINDOW_WIDTH = 800
GAME_HEIGHT = 860
GAME_HEIGHT_OFFSET = 60
GAME_WIDTH = 800
BLOCK_SIZE = 20
SPEED = 10

class SnakeGame():

    # INITIALIZE GAME
    def __init__(self):
        self.w = WINDOW_WIDTH
        self.h = WINDOW_HEIGHT
        self.gw = GAME_WIDTH
        self.gh = GAME_HEIGHT

        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

        self.reset()

    # RESET FUNCTION
    def reset(self):
        self.direction = Direction.RIGHT
        
        # SNAKE INITIAL STATE
        self.head = Point(self.gw / 2, (self.gh / 2) + GAME_HEIGHT_OFFSET / 2)
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (BLOCK_SIZE * 2), self.head.y)]
        
        # SNAKE INITIAL SCORE
        self.score = 0
        self.food = None
        self.place_food()
        self.frame_iteration = 0

    # FOOD FUNCTION
    def place_food(self):
        # PLACES FOOD ON MAP; RECURSVIELY CALLS THE FUNCTION WHEN FOOD IS INSIDE SNAKE
        x = random.randrange(0, GAME_WIDTH, BLOCK_SIZE)
        y = random.randrange(GAME_HEIGHT_OFFSET, GAME_HEIGHT, BLOCK_SIZE)
        self.food = Point(x,y)
        if self.food in self.snake:
            self.place_food()
    
    def play(self, action):
        self.frame_iteration += 1
        for event in pygame.event.get():
            # QUIT EVENT
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # PLAYER INPUT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and self.direction != Direction.DOWN:
                    self.direction = Direction.UP
                elif event.key == pygame.K_s and self.direction != Direction.UP:
                    self.direction = Direction.DOWN
                elif event.key == pygame.K_a and self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_d and self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
        
        # MOVE SNAKE
        self.move(self.direction)
        self.snake.insert(0, self.head)

        # GAME OVER CONDITION WHEN A COLLISION HAPPENS
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > (100 * len(self.snake)):
            reward = -10
            game_over = True
            return reward, game_over, self.score
        
        # PLACES FOOD & INCREASES SCORE OR JUST MOVE
        if self.head == self.food:
            self.score += 10
            reward = 10
            self.place_food()
        else:
            self.snake.pop()

        # UPDATE UI AND DECLARE FRAME RATE
        self.update_frame()
        self.clock.tick(SPEED)

        return reward, game_over, self.score
    
    # MOVE SYSTEM
    def move(self, direction):
        x = self.head.x
        y = self.head.y

        # SNAKE MOVEMENT BASED ON DIRECTION
        if direction == Direction.UP:
            y -= BLOCK_SIZE
        if direction == Direction.DOWN:
            y += BLOCK_SIZE
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        if direction == Direction.LEFT:
            x -= BLOCK_SIZE
        
        self.head = Point(x, y)

    # COLLISION DETECTOR
    def is_collision(self):
        # CHECKS COLLISION ON SELF OR BOUNDARIES
        if (self.head.x < 0 or self.head.y < GAME_HEIGHT_OFFSET) or (self.head.x > GAME_WIDTH - 20 or self.head.y > GAME_HEIGHT - 20):
            return True
        if self.head in self.snake[1:]:
            return True
        
        return False
    
    # UPDATE FRAMES
    def update_frame(self):
        self.display.fill('Black')

        # CREATES A GRID
        for x in range(0, GAME_WIDTH, BLOCK_SIZE):
            for y in range(GAME_HEIGHT_OFFSET, GAME_HEIGHT, BLOCK_SIZE):
                grid_rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(self.display, 'gray9', grid_rect, 1)

        # DISPLAYS SNAKE
        for pos in self.snake:
            snake_rect = pygame.Rect((pos.x, pos.y), (BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, 'Green', snake_rect)

        # DISPLAYS APPLE
        apple_rect = pygame.Rect((self.food.x, self.food.y), (BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.display, 'Red', apple_rect)

        # DISPLAYS SCORE
        score_text = score_font.render("Score: " + str(self.score), True, 'White')
        self.display.blit(score_text, (20, 20))

        pygame.display.flip()


if __name__ == '__main__':
    game = SnakeGame()

    while True:
        game_over, score = game.play()

        if game_over == True:
            break
    
    print('Final Score:', score)

    pygame.quit()
    exit()