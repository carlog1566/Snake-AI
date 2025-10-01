import os
import pygame
import random
from sys import exit
from enum import Enum
from collections import namedtuple

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

    def __init__(self):
        self.w = WINDOW_WIDTH
        self.h = WINDOW_HEIGHT
        self.gw = GAME_WIDTH
        self.gh = GAME_HEIGHT

        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

        self.direction = Direction.RIGHT
        
        self.head = Point(self.gw / 2, (self.gh / 2) + GAME_HEIGHT_OFFSET / 2)
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (BLOCK_SIZE * 2), self.head.y)]
        
        self.score = 0
        self.food = None
        self.place_food()

    def place_food(self):
        x = random.randrange(0, GAME_WIDTH, BLOCK_SIZE)
        y = random.randrange(GAME_HEIGHT_OFFSET, GAME_HEIGHT, BLOCK_SIZE)
        self.food = Point(x,y)
        if self.food in self.snake:
            self.place_food()
    
    def play(self):
        for event in pygame.event.get():
            # QUIT EVENT
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # PLAYER INPUT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.direction = Direction.UP
                elif event.key == pygame.K_s:
                    self.direction = Direction.DOWN
                elif event.key == pygame.K_a:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_d:
                    self.direction = Direction.RIGHT
        
        self.move(self.direction)
        self.snake.insert(0, self.head)

        game_over = False
        if self.is_collision():
            game_over = True
            return game_over, self.score
        
        if self.head == self.food:
            self.score += 10
            self.place_food()
        else:
            self.snake.pop()

        self.update_frame()
        self.clock.tick(SPEED)

        return game_over, self.score
    
    def move(self, direction):
        x = self.head.x
        y = self.head.y

        if direction == Direction.UP:
            y -= BLOCK_SIZE
        if direction == Direction.DOWN:
            y += BLOCK_SIZE
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        if direction == Direction.LEFT:
            x -= BLOCK_SIZE
        
        self.head = Point(x, y)

    def is_collision(self):
        if (self.head.x < 0 or self.head.y < GAME_HEIGHT_OFFSET) or (self.head.x > GAME_WIDTH - 20 or self.head.y > GAME_HEIGHT - 20):
            return True
        if self.head in self.snake[1:]:
            return True
        
        return False
    
    def update_frame(self):
        self.display.fill('Black')

        for x in range(0, GAME_WIDTH, BLOCK_SIZE):
            for y in range(GAME_HEIGHT_OFFSET, GAME_HEIGHT, BLOCK_SIZE):
                grid_rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(self.display, 'gray9', grid_rect, 1)

        for pos in self.snake:
            snake_rect = pygame.Rect((pos.x, pos.y), (BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, 'Green', snake_rect)

        apple_rect = pygame.Rect((self.food.x, self.food.y), (BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.display, 'Red', apple_rect)

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