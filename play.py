import torch
import numpy as np
from snake_game import SnakeGameAI, Direction, Point
from model import Linear_QNet
import os

class PlayAgent:
    def __init__(self, model_path='./model/model.pth'):
        self.model = Linear_QNet(11, 256, 3)
        if os.path.exists(model_path):
            self.model.load_state_dict(torch.load(model_path))
            print(f"Modèle chargé depuis {model_path}")
        else:
            print("Aucun modèle trouvé, utilisation de poids aléatoires")
        self.model.eval()

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
            # Danger tout droit
            (dir_r and game.is_collision(point_r)) or 
            (dir_l and game.is_collision(point_l)) or 
            (dir_u and game.is_collision(point_u)) or 
            (dir_d and game.is_collision(point_d)),

            # Danger à droite
            (dir_u and game.is_collision(point_r)) or 
            (dir_d and game.is_collision(point_l)) or 
            (dir_l and game.is_collision(point_u)) or 
            (dir_r and game.is_collision(point_d)),

            # Danger à gauche
            (dir_d and game.is_collision(point_r)) or 
            (dir_u and game.is_collision(point_l)) or 
            (dir_r and game.is_collision(point_u)) or 
            (dir_l and game.is_collision(point_d)),
            
            # Direction de mouvement
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Emplacement de la nourriture
            game.food.x < game.head.x,  # nourriture à gauche
            game.food.x > game.head.x,  # nourriture à droite
            game.food.y < game.head.y,  # nourriture en haut
            game.food.y > game.head.y   # nourriture en bas
            ]

        return np.array(state, dtype=int)

    def get_action(self, state):
        state0 = torch.tensor(state, dtype=torch.float)
        prediction = self.model(state0)
        move = torch.argmax(prediction).item()
        final_move = [0, 0, 0]
        final_move[move] = 1
        return final_move

def play():
    agent = PlayAgent()
    game = SnakeGameAI()
    
    while True:
        # Obtenir l'état actuel
        state = agent.get_state(game)
        
        # Obtenir l'action de l'IA
        action = agent.get_action(state)
        
        # Effectuer l'action
        reward, done, score = game.play_step(action)
        
        if done:
            print(f'Jeu terminé! Score final: {score}')
            game.reset()

if __name__ == '__main__':
    play() 