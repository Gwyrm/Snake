import torch
import pygame
import sys
import importlib
from helper import plot
import math

class UniversalGUITrainer:
    """
    Système universel pour entraîner n'importe quel agent Snake avec interface graphique
    """
    
    def __init__(self, agent_class, agent_module=None, game_class=None, game_module=None):
        """
        Initialise le trainer universel
        
        Args:
            agent_class: Nom de la classe agent (str) ou classe directement
            agent_module: Module contenant l'agent (optionnel si classe fournie)
            game_class: Nom de la classe jeu (str) ou classe directement (optionnel)
            game_module: Module contenant le jeu (optionnel)
        """
        # Import de l'agent
        if isinstance(agent_class, str):
            if agent_module:
                module = importlib.import_module(agent_module)
                self.agent_class = getattr(module, agent_class)
            else:
                # Chercher dans les modules standards
                try:
                    from agent import Agent
                    from improved_agent import ImprovedAgent
                    from enhanced_training import EnhancedAgent
                    
                    agents = {
                        'Agent': Agent,
                        'ImprovedAgent': ImprovedAgent,
                        'EnhancedAgent': EnhancedAgent
                    }
                    
                    if agent_class in agents:
                        self.agent_class = agents[agent_class]
                    else:
                        raise ValueError(f"Agent {agent_class} non trouvé")
                except ImportError as e:
                    raise ImportError(f"Impossible d'importer l'agent {agent_class}: {e}")
        else:
            self.agent_class = agent_class
        
        # Import du jeu
        if game_class:
            if isinstance(game_class, str):
                if game_module:
                    module = importlib.import_module(game_module)
                    self.game_class = getattr(module, game_class)
                else:
                    from snake_game import SnakeGameAI
                    self.game_class = SnakeGameAI
            else:
                self.game_class = game_class
        else:
            from snake_game import SnakeGameAI
            self.game_class = SnakeGameAI
        
        # Variables de tracking
        self.scores = []
        self.mean_scores = []
        self.total_score = 0
        self.record = 0
        
    def detect_agent_features(self, agent):
        """Détecte automatiquement les fonctionnalités de l'agent"""
        features = {
            'has_get_state': hasattr(agent, 'get_state'),
            'has_get_action': hasattr(agent, 'get_action'),
            'has_get_reward': hasattr(agent, 'get_reward'),
            'has_remember': hasattr(agent, 'remember'),
            'has_train_long_memory': hasattr(agent, 'train_long_memory'),
            'has_train_short_memory': hasattr(agent, 'train_short_memory'),
            'enhanced_play_step': False
        }
        
        # Détecter si le jeu supporte play_step enrichi
        game = self.game_class()
        test_result = game.play_step([1, 0, 0])
        if len(test_result) > 3:
            features['enhanced_play_step'] = True
        
        return features
    
    def get_agent_info(self, agent):
        """Récupère les informations de l'agent pour l'affichage"""
        agent_name = type(agent).__name__
        
        info = {
            'name': agent_name,
            'architecture': 'Inconnue',
            'features': []
        }
        
        # Détecter l'architecture
        if hasattr(agent, 'model'):
            if hasattr(agent.model, 'fc1'):
                input_size = agent.model.fc1.in_features
                hidden_size = agent.model.fc1.out_features
                output_size = agent.model.fc3.out_features if hasattr(agent.model, 'fc3') else agent.model.fc2.out_features
                info['architecture'] = f"{input_size}→{hidden_size}→{output_size}"
        
        # Détecter les fonctionnalités spéciales
        if hasattr(agent, 'count_free_spaces'):
            info['features'].append('Flood Fill')
        if hasattr(agent, 'gamma') and agent.gamma > 0.9:
            info['features'].append('Long-term Planning')
        if hasattr(agent, 'epsilon'):
            info['features'].append('ε-greedy')
            
        return info
    
    def train_with_gui(self, model_save_name=None, max_games=None):
        """Lance l'entraînement avec interface graphique"""
        
        # Initialisation
        agent = self.agent_class()
        game = self.game_class()
        features = self.detect_agent_features(agent)
        agent_info = self.get_agent_info(agent)
        
        print("🎮 UNIVERSAL GUI TRAINER")
        print("=" * 60)
        print(f"🤖 Agent: {agent_info['name']}")
        print(f"🧠 Architecture: {agent_info['architecture']}")
        if agent_info['features']:
            print(f"⚡ Fonctionnalités: {', '.join(agent_info['features'])}")
        print(f"🎯 Jeu: {type(game).__name__}")
        print("=" * 60)
        
        if not model_save_name:
            model_save_name = f"{agent_info['name'].lower()}_model.pth"
        
        while True:
            # Récupération de l'état
            if features['has_get_state']:
                state_old = agent.get_state(game)
            else:
                raise NotImplementedError("L'agent doit avoir une méthode get_state")
            
            # Action
            if features['has_get_action']:
                final_move = agent.get_action(state_old)
            else:
                raise NotImplementedError("L'agent doit avoir une méthode get_action")
            
            # Exécution du mouvement
            if features['enhanced_play_step']:
                # Version enrichie avec distance
                result = game.play_step(final_move)
                if len(result) == 5:
                    basic_reward, done, score, old_distance, new_distance = result
                else:
                    basic_reward, done, score = result[:3]
                    old_distance = new_distance = 0
            else:
                # Version standard
                basic_reward, done, score = game.play_step(final_move)
                old_distance = new_distance = 0
            
            # Nouvel état
            state_new = agent.get_state(game)
            
            # Calcul de la récompense
            if features['has_get_reward']:
                reward = agent.get_reward(game, old_distance, new_distance, basic_reward, done)
            else:
                reward = basic_reward
            
            # Entraînement court terme
            if features['has_train_short_memory']:
                agent.train_short_memory(state_old, final_move, reward, state_new, done)
            
            # Mémorisation
            if features['has_remember']:
                agent.remember(state_old, final_move, reward, state_new, done)
            
            # Fin de jeu
            if done:
                game.reset()
                agent.n_games += 1
                
                # Entraînement long terme
                if features['has_train_long_memory']:
                    agent.train_long_memory()
                
                # Sauvegarde du record
                if score > self.record:
                    self.record = score
                    if hasattr(agent, 'model') and hasattr(agent.model, 'save'):
                        agent.model.save(model_save_name)
                        print(f"🎉 NOUVEAU RECORD ! Score: {score} (Taille: {score + 3})")
                
                # Statistiques
                self.scores.append(score)
                self.total_score += score
                mean_score = self.total_score / agent.n_games
                self.mean_scores.append(mean_score)
                
                # Affichage
                epsilon_display = int(getattr(agent, 'epsilon', 0))
                
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
                
                print(f"{emoji} Jeu {agent.n_games:3d} | Score: {score:2d} | Record: {self.record:2d} | "
                      f"Moy: {mean_score:.1f} | ε: {epsilon_display:2d}")
                
                # Graphique
                try:
                    plot(self.scores, self.mean_scores)
                except:
                    pass  # Ignorer les erreurs de plot
                
                # Limite optionnelle
                if max_games and agent.n_games >= max_games:
                    break
    
    def quick_test(self, num_games=10):
        """Test rapide sans interface graphique"""
        agent = self.agent_class()
        
        # Version console du jeu si disponible
        try:
            from snake_game import SnakeGameAI
            
            class ConsoleGame(SnakeGameAI):
                def __init__(self):
                    super().__init__(640, 480)
                    # Désactiver pygame pour le test
                    self.display = None
                
                def _update_ui(self):
                    pass  # Pas d'affichage
                
                def play_step(self, action):
                    self.frame_iteration += 1
                    
                    if hasattr(self, '_calculate_distance'):
                        old_distance = self._calculate_distance()
                    else:
                        old_distance = 0
                    
                    self._move(action)
                    self.snake.insert(0, self.head)
                    
                    if hasattr(self, '_calculate_distance'):
                        new_distance = self._calculate_distance()
                    else:
                        new_distance = 0
                    
                    reward = 0
                    game_over = False
                    
                    if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
                        game_over = True
                        reward = -10
                        return reward, game_over, self.score, old_distance, new_distance
                    
                    if self.head == self.food:
                        self.score += 1
                        reward = 10
                        self._place_food()
                    else:
                        self.snake.pop()
                    
                    return reward, game_over, self.score, old_distance, new_distance
                
                def _calculate_distance(self):
                    return math.sqrt((self.head.x - self.food.x)**2 + (self.head.y - self.food.y)**2)
            
            game = ConsoleGame()
            scores = []
            
            print(f"🧪 Test rapide de {type(agent).__name__}")
            
            for i in range(num_games):
                score = 0
                done = False
                game.reset()
                
                while not done:
                    state = agent.get_state(game)
                    action = agent.get_action(state)
                    _, done, score, _, _ = game.play_step(action)
                
                scores.append(score)
                print(f"Jeu {i+1}: {score}")
            
            print(f"📊 Score moyen: {sum(scores)/len(scores):.1f}")
            print(f"🏆 Meilleur: {max(scores)}")
            
        except Exception as e:
            print(f"❌ Erreur lors du test: {e}")

# Fonctions pratiques
def train_agent(agent_name, gui=True, model_name=None, max_games=None):
    """Interface simple pour entraîner un agent"""
    trainer = UniversalGUITrainer(agent_name)
    if gui:
        trainer.train_with_gui(model_name, max_games)
    else:
        trainer.quick_test()

def list_available_agents():
    """Liste les agents disponibles"""
    agents = []
    try:
        from agent import Agent
        agents.append(('Agent', 'agent.py - Agent original'))
    except:
        pass
    
    try:
        from improved_agent import ImprovedAgent  
        agents.append(('ImprovedAgent', 'improved_agent.py - Agent amélioré'))
    except:
        pass
    
    try:
        from enhanced_training import EnhancedAgent
        agents.append(('EnhancedAgent', 'enhanced_training.py - Agent enhanced'))
    except:
        pass
    
    print("🤖 Agents disponibles:")
    for name, desc in agents:
        print(f"   • {name}: {desc}")
    
    return [name for name, _ in agents]

if __name__ == '__main__':
    if len(sys.argv) > 1:
        agent_name = sys.argv[1]
        train_agent(agent_name)
    else:
        print("Usage: python universal_gui_trainer.py <nom_agent>")
        print()
        list_available_agents()
        print("\nExemples:")
        print("  python universal_gui_trainer.py Agent")
        print("  python universal_gui_trainer.py ImprovedAgent")
        print("  python universal_gui_trainer.py EnhancedAgent") 