import torch
import random
import numpy as np
from collections import deque
from snake_game_ai import SnakeGame, Direction, Point
from model import Linear_QNet, QTrainer

MAX_MEMORY = 100000
BATCH_SIZE = 1000
LEARNING_RATE = 0.001

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # Controls Randomness
        self.gamma = 0.9 # Discount Rate (must be smaller than 1)
        self.memory = deque(maxlen=MAX_MEMORY) # Removes elements from the left when we exceed memory (popleft())
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, learning_rate=LEARNING_RATE, gamma=self.gamma)


    def get_state(self, game):
        head = game.snake[0]
        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)

        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN
        
        state = [
            # DANGER STRAIGHT
            (dir_r and game.is_collision(point_r)) or
            (dir_l and game.is_collision(point_l)) or
            (dir_u and game.is_collision(point_u)) or
            (dir_d and game.is_collision(point_d)),

            # DANGER RIGHT
            (dir_u and game.is_collision(point_r)) or
            (dir_d and game.is_collision(point_l)) or
            (dir_l and game.is_collision(point_u)) or
            (dir_r and game.is_collision(point_d)),


            # DANGER LEFT
            (dir_d and game.is_collision(point_r)) or
            (dir_u and game.is_collision(point_l)) or
            (dir_r and game.is_collision(point_u)) or
            (dir_l and game.is_collision(point_d)),

            # MOVE DIRECTION
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            # FOOD LOCATION
            game.food.x < game.head.x, # Left
            game.food.x > game.head.x, # Right
            game.food.y < game.head.y, # Up
            game.food.y > game.head.y # Down
        ]

        return np.array(state, dtype=int)


    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over))


    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # Returns list of tuples
        else:
            mini_sample = self.memory 

        states, actions, rewards, next_states, game_overs = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)


    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)


    def get_action(self, state):
        # Random moves: tradeoff exploration / explotation (explore environment first then as the model gets better, we exploit our model/less random moves)
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        
        return final_move
    

def train():
    scores = []
    mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGame()

    while True:
        # GET OLD STATE
        state_old = Agent.get_state(game)

        # GET MOVE FROM OLD STATE
        final_move = agent.get_action(state_old)

        # PERFORM THE MOVE AND GET A NEW STATE
        reward, game_over, score = game.play(final_move)
        state_new = agent.get_state(game)

        # TRAIN SHORT MEMORY
        agent.train_short_memory(state_old, final_move, reward, state_new, game_over)

        # REMEMBER
        agent.remember(state_old, final_move, reward, state_new, game_over)

        if game_over:
            # TRAIN LONG MEMORY (REPLAYING MEMORY/EXPERIENCE REPLAYING)
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

if __name__ == '__main__':
    train()