🐍 Snake AI

A Snake game built from scratch using Pygame, combined with a Reinforcement Learning AI implemented in PyTorch. The AI progressively learns to play Snake and improve its score over time.


🚀 Features

Fully playable Snake game from scratch.

AI agent trained using Deep Q-Learning (DQN).

Progressive learning: AI improves over episodes.

Real-time AI decision visualization.

Modular code structure for experimentation.


💻 Installation

Clone the repository:

git clone https://github.com/carlog1566/Snake-AI


(Optional) Create a virtual environment:

python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate


Install dependencies manually (you can use pip):

pip install pygame torch numpy matplotlib


🎮 Usage

Play the Game Manually
cd ~/snake_human
python snake_game_human.py

Watch AI Train and Play the Game
cd ~/snake_ai
python snake_agent.py
    - Press repeatedly or hold 'W' to speed up
    - Press 'R' to reset speed


🧠 Reinforcement Learning Details

Algorithm: Deep Q-Learning (DQN)

Reward system:

+10 for eating food

-10 for hitting a wall or self-collision

Progress: AI initially moves randomly and dies quickly. After training, it learns to survive longer and maximize score.


🎯 Future Work

Have the snake sense itself as a danger.

Implement advanced RL algorithms (Double DQN, PPO).

Visualize AI decision-making in real-time.

Optimize AI training performance.

(Maybe) Add obstacles or varied maps to increase difficulty.