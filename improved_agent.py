import torch
import random
import numpy as np
from collections import deque
from snake_game import SnakeGameAI, Direction, Point
from model import Linear_QNet, QTrainer
import math

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class ImprovedAgent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        # État étendu : 16 variables au lieu de 11
        self.model = Linear_QNet(16, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def is_safe_move(self, game, point, depth=3):
        """Vérifie si un mouvement est sûr en regardant plusieurs coups à l'avance"""
        if game.is_collision(point):
            return False
        
        if depth == 0:
            return True
        
        # Compter l'espace libre autour du point
        free_spaces = 0
        for dx, dy in [(0, 20), (0, -20), (20, 0), (-20, 0)]:
            new_point = Point(point.x + dx, point.y + dy)
            if not game.is_collision(new_point):
                free_spaces += 1
        
        # Si moins de 2 sorties, c'est dangereux
        return free_spaces >= 2

    def count_free_spaces(self, game, point, max_distance=100):
        """Compte les espaces libres accessibles depuis un point (algorithme de flood fill)"""
        if game.is_collision(point):
            return 0
        
        visited = set()
        stack = [point]
        count = 0
        
        while stack and count < max_distance:
            current = stack.pop()
            if current in visited:
                continue
            
            if game.is_collision(current):
                continue
                
            visited.add(current)
            count += 1
            
            # Ajouter les voisins
            for dx, dy in [(0, 20), (0, -20), (20, 0), (-20, 0)]:
                neighbor = Point(current.x + dx, current.y + dy)
                if neighbor not in visited:
                    stack.append(neighbor)
        
        return count

    def get_state(self, game):
        head = game.snake[0]
        
        # Points autour de la tête
        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)
        
        # Directions actuelles
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        # Distance à la nourriture
        food_distance = math.sqrt((head.x - game.food.x)**2 + (head.y - game.food.y)**2)
        
        # État étendu avec plus d'informations
        state = [
            # Danger immédiat (collision directe)
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
            
            # Directions actuelles
            dir_l, dir_r, dir_u, dir_d,
            
            # Position de la nourriture
            game.food.x < game.head.x,  # nourriture à gauche
            game.food.x > game.head.x,  # nourriture à droite
            game.food.y < game.head.y,  # nourriture en haut
            game.food.y > game.head.y,  # nourriture en bas
            
            # NOUVELLES FEATURES pour éviter les pièges
            # Danger de piège (peu d'espace libre après le mouvement)
            (dir_r and self.count_free_spaces(game, point_r, 20) < 5) or
            (dir_l and self.count_free_spaces(game, point_l, 20) < 5) or
            (dir_u and self.count_free_spaces(game, point_u, 20) < 5) or
            (dir_d and self.count_free_spaces(game, point_d, 20) < 5),
            
            # Distance relative à la nourriture (normalisée)
            min(food_distance / 100.0, 1.0),
            
            # Taille du snake (normalisée)
            min(len(game.snake) / 20.0, 1.0)
            ]

        return np.array(state, dtype=float)

    def get_reward(self, game, old_distance, new_distance, reward, done):
        """Système de récompenses amélioré"""
        if done:
            return -10  # Grosse pénalité pour mourir
        
        if reward == 10:  # A mangé de la nourriture
            return 10 + len(game.snake) * 0.5  # Bonus progressif selon la taille
        
        # Récompense pour se rapprocher de la nourriture
        if new_distance < old_distance:
            return 1  # Se rapprocher = bien
        elif new_distance > old_distance:
            return -0.5  # S'éloigner = moins bien
        
        # Petite récompense pour survivre
        return 0.1

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # Epsilon décroissant plus lent pour plus d'exploration
        self.epsilon = max(5, 80 - self.n_games * 0.5)
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

# Version améliorée du jeu avec métriques étendues
class ImprovedSnakeGameAI(SnakeGameAI):
    def __init__(self, w=640, h=480):
        super().__init__(w, h)
        self.prev_distance_to_food = 0

    def reset(self):
        super().reset()
        self.prev_distance_to_food = math.sqrt((self.head.x - self.food.x)**2 + (self.head.y - self.food.y)**2)

    def play_step(self, action):
        self.frame_iteration += 1
        
        # Calculer la distance avant le mouvement
        old_distance = math.sqrt((self.head.x - self.food.x)**2 + (self.head.y - self.food.y)**2)
        
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # Bouger
        self._move(action)
        self.snake.insert(0, self.head)
        
        # Calculer la nouvelle distance
        new_distance = math.sqrt((self.head.x - self.food.x)**2 + (self.head.y - self.food.y)**2)
        
        # Vérifier game over
        reward = 0
        game_over = False
        
        # Timeout plus généreux pour les snakes longs
        timeout = 100 * len(self.snake) + 50
        if self.is_collision() or self.frame_iteration > timeout:
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # Manger la nourriture
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
            new_distance = math.sqrt((self.head.x - self.food.x)**2 + (self.head.y - self.food.y)**2)
        else:
            self.snake.pop()
        
        # Mise à jour de l'affichage
        self._update_ui()
        self.clock.tick(SPEED)
        
        return reward, game_over, self.score, old_distance, new_distance

def improved_train():
    scores = []
    mean_scores = []
    total_score = 0
    record = 0
    agent = ImprovedAgent()
    game = ImprovedSnakeGameAI()
    
    print("🐍 Entraînement Snake AI AMÉLIORÉ...")
    print("=" * 60)
    print("Nouvelles fonctionnalités :")
    print("- Détection de pièges avancée")
    print("- Système de récompenses progressif")
    print("- État étendu (16 variables)")
    print("- Prévention de l'auto-collision")
    print("=" * 60)
    
    while True:
        # État actuel
        state_old = agent.get_state(game)

        # Action
        final_move = agent.get_action(state_old)

        # Exécuter l'action
        result = game.play_step(final_move)
        if len(result) == 5:
            basic_reward, done, score, old_distance, new_distance = result
        else:
            basic_reward, done, score = result
            old_distance = new_distance = 0
        
        # Nouveau état
        state_new = agent.get_state(game)
        
        # Récompense améliorée
        reward = agent.get_reward(game, old_distance, new_distance, basic_reward, done)

        # Entraînement court terme
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # Mémoriser
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # Entraînement long terme
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save('improved_model.pth')
                print(f"🎉 NOUVEAU RECORD ! Score: {score}")

            scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            mean_scores.append(mean_score)
            
            # Affichage amélioré
            epsilon_display = max(0, int(agent.epsilon))
            print(f"Jeu {agent.n_games:3d} | Score: {score:2d} | Record: {record:2d} | "
                  f"Moy: {mean_score:.1f} | ε: {epsilon_display:2d} | "
                  f"Mémoire: {len(agent.memory):5d}")
            
            # Stats détaillées tous les 50 jeux
            if agent.n_games % 50 == 0:
                print("-" * 60)
                recent_scores = scores[-50:] if len(scores) >= 50 else scores
                recent_avg = sum(recent_scores) / len(recent_scores)
                max_recent = max(recent_scores) if recent_scores else 0
                print(f"📊 Stats (50 derniers) - Moyenne: {recent_avg:.1f} | "
                      f"Max: {max_recent} | Global: {mean_score:.1f}")
                print(f"💾 Modèle sauvegardé | 🧠 Mémoire: {len(agent.memory)}/{MAX_MEMORY}")
                print("-" * 60)

if __name__ == '__main__':
    # Importer pygame seulement si nécessaire
    import pygame
    SPEED = 40
    improved_train() 