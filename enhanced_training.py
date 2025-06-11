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

class EnhancedAgent:
    """Agent optimisé combinant les avantages des deux approches"""
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.95  # Facteur de discount plus élevé pour récompenses à long terme
        self.memory = deque(maxlen=MAX_MEMORY)
        # 16 variables d'état mais architecture plus grande
        self.model = Linear_QNet(16, 512, 3)  # Plus de neurones cachés
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def count_free_spaces(self, game, point, max_distance=20):
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
            
            for dx, dy in [(0, 20), (0, -20), (20, 0), (-20, 0)]:
                neighbor = Point(current.x + dx, current.y + dy)
                if neighbor not in visited:
                    stack.append(neighbor)
        
        return count

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

        food_distance = math.sqrt((head.x - game.food.x)**2 + (head.y - game.food.y)**2)
        
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
            
            dir_l, dir_r, dir_u, dir_d,
            
            game.food.x < game.head.x,
            game.food.x > game.head.x,
            game.food.y < game.head.y,
            game.food.y > game.head.y,
            
            # Features avancées mais moins restrictives
            (dir_r and self.count_free_spaces(game, point_r, 10) < 3) or
            (dir_l and self.count_free_spaces(game, point_l, 10) < 3) or
            (dir_u and self.count_free_spaces(game, point_u, 10) < 3) or
            (dir_d and self.count_free_spaces(game, point_d, 10) < 3),
            
            min(food_distance / 300.0, 1.0),  # Normalisé différemment
            min(len(game.snake) / 30.0, 1.0),  # Permet des snakes plus longs
            self.count_free_spaces(game, head, 15) / 15.0,
            min(head.x / game.w, (game.w - head.x) / game.w, 
                head.y / game.h, (game.h - head.y) / game.h)
        ]

        return np.array(state, dtype=float)

    def get_reward(self, game, old_distance, new_distance, reward, done):
        """Système de récompenses optimisé pour encourager les hauts scores"""
        if done:
            return -15  # Pénalité plus sévère pour mourir
        
        if reward == 10:  # A mangé de la nourriture
            # Bonus progressif plus agressif
            return 20 + len(game.snake) * 1.0
        
        # Récompenses plus généreuses pour se rapprocher
        if new_distance < old_distance:
            return 2.0  # Plus de récompense pour se rapprocher
        elif new_distance > old_distance:
            return -1.0  # Pénalité pour s'éloigner
        
        # Bonus de survie plus important
        return 0.2

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
        # Exploration plus agressive au début, puis exploitation
        self.epsilon = max(2, 100 - self.n_games * 0.8)
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

class EnhancedSnakeGameAI_Console(SnakeGameAI):
    """Version console optimisée"""
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.reset()

    def play_step(self, action):
        self.frame_iteration += 1
        
        old_distance = math.sqrt((self.head.x - self.food.x)**2 + (self.head.y - self.food.y)**2)
        
        self._move(action)
        self.snake.insert(0, self.head)
        
        new_distance = math.sqrt((self.head.x - self.food.x)**2 + (self.head.y - self.food.y)**2)
        
        reward = 0
        game_over = False
        
        # Timeout plus généreux pour encourager de longs snakes
        timeout = 150 * len(self.snake) + 200
        if self.is_collision() or self.frame_iteration > timeout:
            game_over = True
            reward = -10
            return reward, game_over, self.score, old_distance, new_distance

        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
            new_distance = math.sqrt((self.head.x - self.food.x)**2 + (self.head.y - self.food.y)**2)
        else:
            self.snake.pop()
        
        return reward, game_over, self.score, old_distance, new_distance

def enhanced_train():
    scores = []
    mean_scores = []
    total_score = 0
    record = 0
    agent = EnhancedAgent()
    game = EnhancedSnakeGameAI_Console()
    
    print("🚀 ENTRAÎNEMENT SNAKE AI OPTIMISÉ")
    print("=" * 70)
    print("🎯 Objectif: Combiner stabilité ET haute performance")
    print("📈 Améliorations:")
    print("   • Architecture plus large (512 neurones)")
    print("   • Gamma plus élevé (0.95)")
    print("   • Récompenses optimisées")
    print("   • Exploration agressive puis exploitation")
    print("   • Timeouts généreux")
    print("=" * 70)
    
    best_avg_50 = 0
    games_without_improvement = 0
    
    while agent.n_games < 500:  # Entraînement plus long
        state_old = agent.get_state(game)
        final_move = agent.get_action(state_old)

        result = game.play_step(final_move)
        basic_reward, done, score, old_distance, new_distance = result
        
        state_new = agent.get_state(game)
        reward = agent.get_reward(game, old_distance, new_distance, basic_reward, done)

        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save('enhanced_model.pth')
                print(f"🎉 NOUVEAU RECORD ! Score: {score} (Taille: {score + 3})")

            scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            mean_scores.append(mean_score)
            
            # Analyser les derniers 50 jeux
            if len(scores) >= 50:
                recent_50 = scores[-50:]
                avg_50 = sum(recent_50) / 50
                if avg_50 > best_avg_50:
                    best_avg_50 = avg_50
                    games_without_improvement = 0
                else:
                    games_without_improvement += 1
            
            epsilon_display = max(0, int(agent.epsilon))
            
            # Émojis selon performance
            if score >= 50:
                emoji = "🔥"
            elif score >= 30:
                emoji = "🚀"
            elif score >= 15:
                emoji = "⭐"
            elif score >= 5:
                emoji = "✅"
            else:
                emoji = "🎯"
            
            print(f"{emoji} Jeu {agent.n_games:3d} | Score: {score:2d} | Record: {record:2d} | "
                  f"Moy: {mean_score:.1f} | ε: {epsilon_display:2d} | "
                  f"Mémoire: {len(agent.memory):5d}")
            
            # Stats tous les 50 jeux
            if agent.n_games % 50 == 0:
                print("-" * 70)
                recent_avg = sum(scores[-50:]) / 50 if len(scores) >= 50 else mean_score
                max_recent = max(scores[-50:]) if len(scores) >= 50 else record
                
                print(f"📊 Stats (50 derniers) - Moyenne: {recent_avg:.1f} | "
                      f"Max: {max_recent} | Global: {mean_score:.1f}")
                print(f"💾 Modèle sauvegardé | Best avg 50: {best_avg_50:.1f}")
                
                # Évaluation de performance
                if recent_avg > 25:
                    print("🏆 Performance EXCELLENTE ! IA de niveau expert")
                elif recent_avg > 15:
                    print("🎯 Performance TRÈS BONNE ! IA compétente")
                elif recent_avg > 8:
                    print("📈 Performance BONNE ! IA en progression")
                elif recent_avg > 3:
                    print("🔄 Performance CORRECTE ! IA apprentissage")
                else:
                    print("🔄 Phase d'exploration initiale")
                
                print("-" * 70)
                
                # Arrêt si pas d'amélioration sur 200 jeux
                if games_without_improvement > 200:
                    print("🛑 Arrêt : pas d'amélioration depuis 200 jeux")
                    break
    
    print(f"\n🏁 Entraînement terminé après {agent.n_games} jeux !")
    print(f"📈 Score final moyen: {mean_score:.1f}")
    print(f"🏆 Meilleur score: {record}")
    print(f"🎯 Meilleure moyenne sur 50 jeux: {best_avg_50:.1f}")
    print(f"💾 Modèle optimisé sauvegardé dans ./model/enhanced_model.pth")

if __name__ == '__main__':
    enhanced_train() 