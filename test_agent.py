import torch
import random
import numpy as np
from collections import deque
from snake_game import SnakeGameAI, Direction, Point
from model import Linear_QNet, QTrainer

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

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

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft si MAX_MEMORY est atteint

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # liste de tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # mouvements aléatoires : compromis exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

# Version simplifiée du jeu sans interface graphique
class SnakeGameAI_Console(SnakeGameAI):
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # Pas d'initialisation d'affichage
        self.reset()

    def play_step(self, action):
        self.frame_iteration += 1
        
        # 2. Bouger
        self._move(action) # Met à jour la tête
        self.snake.insert(0, self.head)
        
        # 3. Vérifier si le jeu est terminé
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. Placer une nouvelle nourriture ou juste bouger
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()
        
        # Pas de mise à jour d'interface
        return reward, game_over, self.score

def test_train():
    scores = []
    mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI_Console()
    
    print("🐍 Début de l'entraînement Snake AI...")
    print("=" * 50)
    
    while agent.n_games < 100:  # Limiter à 100 jeux pour le test
        # obtenir l'ancien état
        state_old = agent.get_state(game)

        # obtenir le mouvement
        final_move = agent.get_action(state_old)

        # effectuer le mouvement et obtenir le nouvel état
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # entraîner la mémoire courte
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # se souvenir
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # entraîner la mémoire longue
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()
                print(f"🎉 NOUVEAU RECORD ! Score: {score}")

            scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            mean_scores.append(mean_score)
            
            # Affichage détaillé
            print(f"Jeu {agent.n_games:3d} | Score: {score:2d} | Record: {record:2d} | Score moyen: {mean_score:.1f} | Epsilon: {agent.epsilon:2d}")
            
            # Affichage de progression tous les 10 jeux
            if agent.n_games % 10 == 0:
                print("-" * 50)
                recent_scores = scores[-10:] if len(scores) >= 10 else scores
                recent_avg = sum(recent_scores) / len(recent_scores)
                print(f"📊 Progression - Derniers 10 jeux: {recent_avg:.1f} | Global: {mean_score:.1f}")
                print("-" * 50)
    
    print("\n🏁 Entraînement terminé !")
    print(f"📈 Score final moyen: {mean_score:.1f}")
    print(f"🏆 Meilleur score: {record}")
    print(f"💾 Modèle sauvegardé dans ./model/model.pth")

if __name__ == '__main__':
    test_train() 