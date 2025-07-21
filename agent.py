import torch
import random
import numpy as np
from collections import deque
from snake_game import SnakeGameAI, Direction
from model import Linear_QNet, QTrainer

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self, hidden_size=256):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(11, hidden_size, 3) # input_size, hidden_size, output_size
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        self.device = self.model.device  # Récupère le device du modèle

    def get_state(self, game):
        return game.get_state()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # Stocker l'état actuel pour la visualisation
        self.last_state = state
        
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
            # Pour les mouvements aléatoires, pas de valeurs de prédiction
            self.last_action_values = [0.0, 0.0, 0.0]
        else:
            state0 = torch.tensor(state, dtype=torch.float).to(self.device)
            prediction = self.model(state0)
            # Stocker les valeurs de prédiction pour la visualisation
            self.last_action_values = prediction.cpu().detach().numpy().tolist()
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move
    
    def get_weights(self):
        """Retourne les poids du modèle pour visualisation"""
        return self.model.get_weights()
    
    def get_biases(self):
        """Retourne les biais du modèle pour visualisation"""
        return self.model.get_biases() 