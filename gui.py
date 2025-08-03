import pygame
import numpy as np
import torch
from agent import Agent
from snake_game import SnakeGameAI

class SnakeAIGUI:
    def __init__(self):
        pygame.init()
        
        # Zone d'enregistrement élargie
        self.RECORD_WIDTH = 640  # Élargi de 540 à 640
        self.CONTROLS_WIDTH = 300 # Largeur de la zone de contrôles
        self.WINDOW_WIDTH = self.RECORD_WIDTH + self.CONTROLS_WIDTH  # 940px total
        self.WINDOW_HEIGHT = 1210  # Réduit car suppression légende
        
        # Zone du jeu élargie (partie gauche, enregistrable)
        self.GAME_WIDTH = 560   # Agrandi de 480 à 560
        self.GAME_HEIGHT = 560  # Agrandi de 480 à 560
        self.GAME_X = (self.RECORD_WIDTH - self.GAME_WIDTH) // 2
        self.GAME_Y = 80  # Plus haut, directement sous le texte
        
        # Zone des contrôles (partie droite, hors enregistrement)
        self.CONTROLS_X = self.RECORD_WIDTH + 20  # Début de la zone de contrôles
        self.CONTROLS_Y = self.GAME_Y
        self.CONTROLS_HEIGHT = 400
        
        # Couleurs
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        self.LIGHT_GRAY = (200, 200, 200)
        self.BLUE = (0, 100, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        
        # Initialisation de pygame
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption('Snake AI')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 18)
        
        # Paramètres ajustables
        self.game_speed = 15
        
        # 🔧 CONFIGURATION DU RÉSEAU - Modifiable facilement
        self.hidden_size = 32  # ← CHANGEZ ICI le nombre de neurones cachés (ex: 64, 256, 512)
        
        # Initialisation du jeu et de l'agent
        self.game = SnakeGameAI(w=self.GAME_WIDTH, h=self.GAME_HEIGHT, block_size=20)
        self.agent = Agent(hidden_size=self.hidden_size)
        
        # Variables pour l'entraînement
        self.running = True
        self.training = False
        self.plot_scores = []
        self.total_score = 0
        self.record = 0
        
        # Tracking des poids pour visualisation
        self.weights_history = []
        self.weights_update_interval = 10  # Mise à jour tous les 10 frames
        self.weights_update_counter = 0
        
        # Boutons
        self.buttons = self.create_buttons()
        
        # Démarrage silencieux
        pass
        
    def create_buttons(self):
        """Crée les boutons de contrôle"""
        buttons = []
        
        # Boutons dans la zone de contrôles (partie droite)
        btn_width = 120
        btn_height = 40
        btn_spacing = 15
        
        # Bouton Start/Stop
        start_btn = {
            'rect': pygame.Rect(self.CONTROLS_X, self.CONTROLS_Y + 20, btn_width, btn_height),
            'text': 'START',
            'action': 'toggle_training',
            'color': self.GREEN
        }
        buttons.append(start_btn)
        
        # Bouton Reset
        reset_btn = {
            'rect': pygame.Rect(self.CONTROLS_X, self.CONTROLS_Y + 20 + btn_height + btn_spacing, btn_width, btn_height),
            'text': 'RESET',
            'action': 'reset_training',
            'color': self.RED
        }
        buttons.append(reset_btn)
        
        # Contrôles de vitesse
        speed_normal = {
            'rect': pygame.Rect(self.CONTROLS_X, self.CONTROLS_Y + 20 + 2*(btn_height + btn_spacing), btn_width, btn_height),
            'text': 'NORMAL',
            'action': 'speed_normal',
            'color': self.BLUE
        }
        buttons.append(speed_normal)
        
        speed_fast = {
            'rect': pygame.Rect(self.CONTROLS_X, self.CONTROLS_Y + 20 + 3*(btn_height + btn_spacing), btn_width, btn_height),
            'text': 'RAPIDE',
            'action': 'speed_fast',
            'color': self.RED
        }
        buttons.append(speed_fast)
        
        return buttons
    
    def handle_button_click(self, pos):
        """Gère les clics sur les boutons"""
        for button in self.buttons:
            if button['rect'].collidepoint(pos):
                action = button['action']
                
                if action == 'toggle_training':
                    self.training = not self.training
                    button['text'] = 'STOP' if self.training else 'START'
                    button['color'] = self.RED if self.training else self.GREEN
                    
                elif action == 'reset_training':
                    self.reset_training()
                    
                elif action == 'speed_normal':
                    self.game_speed = 15
                    
                elif action == 'speed_fast':
                    self.game_speed = 60
    
    def reset_training(self):
        """Remet à zéro l'entraînement"""
        self.agent = Agent(hidden_size=self.hidden_size)
        self.game.reset()
        self.plot_scores = []
        self.total_score = 0
        self.record = 0
        self.agent.n_games = 0
        
    def train_step(self):
        """Effectue une étape d'entraînement"""
        if not self.training:
            return
            
        # get old state
        state_old = self.agent.get_state(self.game)

        # get move
        final_move = self.agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = self.game.play_step(final_move)
        state_new = self.agent.get_state(self.game)

        # train short memory
        self.agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        self.agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            self.game.reset()
            self.agent.n_games += 1
            self.agent.train_long_memory()

            if score > self.record:
                self.record = score

            self.plot_scores.append(score)
            self.total_score += score
        
        # Mise à jour des poids (tous les N frames pour la performance)
        self.weights_update_counter += 1
        if self.weights_update_counter >= self.weights_update_interval:
            self.weights_update_counter = 0
            
            # Récupérer les poids actuels
            weights = self.agent.model.get_weights()
            biases = self.agent.model.get_biases()
            weights2 = self.agent.model.get_layer2_weights()
            biases2 = self.agent.model.get_layer2_biases()
            
            # Calculer les statistiques
            weights_stats = {
                'layer1_mean': np.mean(np.abs(weights)),
                'layer1_std': np.std(weights),
                'layer1_max': np.max(np.abs(weights)),
                'layer2_mean': np.mean(np.abs(weights2)),
                'layer2_std': np.std(weights2),
                'layer2_max': np.max(np.abs(weights2)),
                'total_magnitude': np.sum(np.abs(weights)) + np.sum(np.abs(biases)) + np.sum(np.abs(weights2)) + np.sum(np.abs(biases2))
            }
            
            self.weights_history.append(weights_stats)
            
            # Limiter l'historique (garder seulement les 100 dernières mesures)
            if len(self.weights_history) > 100:
                self.weights_history = self.weights_history[-100:]
    
    def draw_beautiful_graph(self):
        """Dessine un graphique moderne et élégant"""
        # Zone de graphique (reste dans la zone d'enregistrement)
        graph_area = pygame.Rect(30, self.GAME_Y + self.GAME_HEIGHT + 30, self.RECORD_WIDTH - 60, 180)
        
        # Fond du graphique avec gradient effet
        pygame.draw.rect(self.screen, (20, 20, 40), graph_area)
        pygame.draw.rect(self.screen, (40, 40, 80), graph_area, 2)
        
        # Titre du graphique
        title = self.font.render('Evolution des Scores', True, (100, 200, 255))
        title_rect = title.get_rect(center=(graph_area.centerx, graph_area.top + 20))
        self.screen.blit(title, title_rect)
        
        # Zone de dessin du graphique
        plot_area = pygame.Rect(graph_area.left + 40, graph_area.top + 40, 
                               graph_area.width - 80, graph_area.height - 80)
        
        if len(self.plot_scores) > 1:
            # Prendre les 20 derniers scores
            recent_scores = self.plot_scores[-20:]
            max_score = max(recent_scores) if recent_scores and max(recent_scores) > 0 else 1
            
            # Calculer les points du graphique
            points = []
            for i, score in enumerate(recent_scores):
                x = plot_area.left + (i * plot_area.width) // len(recent_scores)
                y = plot_area.bottom - int((score / max_score) * plot_area.height)
                points.append((x, y))
            
            # Dessiner la ligne du graphique avec effet glow
            if len(points) > 1:
                # Ligne principale
                pygame.draw.lines(self.screen, (0, 255, 150), False, points, 3)
                
                # Effet glow (lignes plus fines autour)
                for offset in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    glow_points = [(p[0] + offset[0], p[1] + offset[1]) for p in points]
                    pygame.draw.lines(self.screen, (0, 150, 100), False, glow_points, 1)
                
                # Points sur la courbe
                for i, point in enumerate(points):
                    if i == len(points) - 1:  # Dernier point en surbrillance
                        pygame.draw.circle(self.screen, (255, 255, 0), point, 5)
                        pygame.draw.circle(self.screen, (255, 150, 0), point, 3)
                    else:
                        pygame.draw.circle(self.screen, (0, 255, 150), point, 3)
                        pygame.draw.circle(self.screen, (0, 200, 120), point, 2)
    
    def draw_weights_visualization(self):
        """Dessine une visualisation du réseau de neurones avec des couleurs représentant les poids"""
        # Zone pour les poids (directement sous le graphique des scores)
        graph_area = pygame.Rect(30, self.GAME_Y + self.GAME_HEIGHT + 30, self.RECORD_WIDTH - 60, 180)
        weights_y = graph_area.bottom + 20  # Directement sous le graphique
        weights_area = pygame.Rect(20, weights_y, self.RECORD_WIDTH - 40, 250)  # Agrandi à 250px de hauteur
        
        # Fond avec gradient et bordure moderne
        pygame.draw.rect(self.screen, (15, 15, 30), weights_area)  # Fond plus sombre
        pygame.draw.rect(self.screen, (60, 60, 100), weights_area, 3)  # Bordure plus épaisse
        
        # Titre avec l'architecture réelle (corrigée)
        if len(self.weights_history) > 0:
            try:
                weights1 = self.agent.model.get_weights()
                weights2 = self.agent.model.get_layer2_weights()
                input_neurons = weights1.shape[1]  # Nombre réel d'inputs (in_features de linear1)
                real_hidden_neurons = weights1.shape[0]  # Nombre réel de neurones cachés (out_features de linear1)
                output_neurons = weights2.shape[0]  # Nombre réel d'outputs (out_features de linear2)
                config_text = f'Reseau {input_neurons}-{real_hidden_neurons}-{output_neurons}'
            except:
                config_text = f'Reseau {self.hidden_size}N'
        else:
            config_text = f'Reseau {self.hidden_size}N'
            
        # title = self.small_font.render(config_text, True, (100, 200, 255))
        # title_rect = title.get_rect(center=(weights_area.centerx, weights_area.top + 15))
        # self.screen.blit(title, title_rect)
        
        if len(self.weights_history) > 0:
            # Zone pour le réseau (décalée à droite pour les labels)
            network_area = pygame.Rect(weights_area.left + 100, weights_area.top + 25,  # Encore plus d'espace à gauche
                                     weights_area.width - 200, 180)  # Agrandi à 180px de hauteur
            
            # Récupérer les poids actuels
            try:
                weights1 = self.agent.model.get_weights()  # 11 x 128
                weights2 = self.agent.model.get_layer2_weights()  # 128 x 3
                
                # Normaliser les poids pour les couleurs (entre 0 et 1)
                w1_norm = np.abs(weights1) / (np.max(np.abs(weights1)) + 1e-8)
                w2_norm = np.abs(weights2) / (np.max(np.abs(weights2)) + 1e-8)
                
                # Positions des neurones (dynamiques basées sur le modèle réel)
                # ATTENTION: PyTorch stocke les poids en (out_features, in_features)
                input_neurons = weights1.shape[1]  # Nombre réel d'inputs (in_features de linear1)
                real_hidden_neurons = weights1.shape[0]  # Nombre réel de neurones cachés (out_features de linear1)
                output_neurons = weights2.shape[0]  # Nombre réel d'outputs (out_features de linear2)
                
                # Limiter l'affichage pour la lisibilité mais rester proportionnel
                hidden_neurons = real_hidden_neurons
                
                # Debug uniquement si changement (éviter le spam)
                # print(f"Réseau: {input_neurons} → {real_hidden_neurons} → {output_neurons} (affichage: {hidden_neurons} cachés)")
                
                # Calculer les positions avec plus d'espace
                layer_width = network_area.width // 3
                
                # Couche d'entrée (gauche) - avec espace pour labels seulement
                input_x = network_area.left + layer_width // 10  # Plus d'espace à gauche
                input_y_start = network_area.top + 10
                input_spacing = (network_area.height - 10) // (input_neurons - 1) if input_neurons > 1 else 0
                
                # Couche cachée (centre) 
                hidden_x = network_area.left + layer_width + layer_width // 2
                hidden_y_start = network_area.top + 10  # Plus d'espace en haut
                hidden_spacing = (network_area.height - 10) // (hidden_neurons - 1) if hidden_neurons > 1 else 0  # Espacement normal
                
                # Augmenter l'espacement en réduisant la zone utilisée
                hidden_neurons_display = hidden_neurons  # Afficher tous les neurones
                if hidden_neurons_display > 1:
                    hidden_spacing = (network_area.height - 10) // (hidden_neurons_display - 1)
                
                # Couche de sortie (droite) - avec espace pour labels seulement
                output_x = network_area.left + 2 * layer_width + 2 * layer_width // 3  # Plus d'espace à droite
                output_y_start = network_area.top + 10
                output_spacing = (network_area.height - 10) // (output_neurons - 1) if output_neurons > 1 else 0
                
                # Dessiner les connexions (input -> hidden) - adaptatif
                connection_step = max(1, real_hidden_neurons // hidden_neurons)  # Échantillonnage intelligent
                
                for i in range(input_neurons):
                    input_pos = (input_x, input_y_start + i * input_spacing)
                    for display_j in range(hidden_neurons_display):
                        # Mapper l'index d'affichage vers l'index réel du réseau
                        real_j = display_j * connection_step
                        if real_j < real_hidden_neurons:
                            hidden_pos = (hidden_x, hidden_y_start + display_j * hidden_spacing)
                            
                            # Couleur basée sur le poids réel (ATTENTION: transposition PyTorch)
                            if real_j < w1_norm.shape[0] and i < w1_norm.shape[1]:
                                weight_val = w1_norm[real_j, i]  # [hidden, input] dans PyTorch
                                
                                # Assurer une visibilité minimale même pour les poids très faibles
                                if weight_val < 0.02:
                                    # Connexions très faibles en gris clair
                                    color = (100, 100, 120)
                                else:
                                    # Connexions normales en jaune->orange->rouge
                                    color_intensity = int(weight_val * 255)
                                    color = (255, 255 - color_intensity, 0)
                                
                                # Afficher TOUTES les connexions
                                pygame.draw.line(self.screen, color, input_pos, hidden_pos, 1)
                
                # Dessiner les connexions (hidden -> output) - TOUTES les connexions
                for display_i in range(hidden_neurons_display):
                    real_i = display_i * connection_step
                    if real_i < real_hidden_neurons:
                        hidden_pos = (hidden_x, hidden_y_start + display_i * hidden_spacing)
                        for j in range(output_neurons):
                            output_pos = (output_x, output_y_start + j * output_spacing)
                            
                            # Couleur basée sur le poids réel
                            if real_i < real_hidden_neurons and j < output_neurons:
                                weight_val = w2_norm[j, real_i]  # [output, hidden] dans PyTorch
                                
                                # Assurer une visibilité minimale même pour les poids très faibles
                                if weight_val < 0.02:
                                    # Connexions très faibles en gris clair
                                    color = (100, 100, 120)
                                else:
                                    # Connexions normales en jaune->orange->rouge
                                    color_intensity = int(weight_val * 255)
                                    color = (255, 255 - color_intensity, 0)
                                
                                # Afficher TOUTES les connexions
                                pygame.draw.line(self.screen, color, hidden_pos, output_pos, 1)
                
                # Labels courts pour le graphique
                input_short_labels = ['DDevant', 'DDroite', 'DGauche', 'DirG', 'DirD', 'DirH', 'DirB', 'FG', 'FD', 'FH', 'FB']
                
                for i in range(input_neurons):
                    pos = (input_x, input_y_start + i * input_spacing)
                    # Neurones d'entrée plus gros
                    pygame.draw.circle(self.screen, (120, 255, 120), pos, 5)
                    pygame.draw.circle(self.screen, (80, 200, 80), pos, 3)
                    
                    # Label court à gauche du neurone
                    if i < len(input_short_labels):
                        label_text = self.font.render(input_short_labels[i], True, (150, 255, 150))
                        self.screen.blit(label_text, (pos[0] - 85, pos[1] - 8))
                
                # Couche cachée
                for i in range(hidden_neurons_display):
                    pos = (hidden_x, hidden_y_start + i * hidden_spacing)
                    # Neurones cachés plus gros
                    pygame.draw.circle(self.screen, (255, 255, 120), pos, 5)
                    pygame.draw.circle(self.screen, (200, 200, 80), pos, 3)
                
                # Couche de sortie avec labels courts et valeurs
                output_short_labels = ['AHaut', 'ADroite', 'AGauche']
                
                for i in range(output_neurons):
                    pos = (output_x, output_y_start + i * output_spacing)
                    # Neurones de sortie encore plus gros
                    pygame.draw.circle(self.screen, (255, 120, 120), pos, 6)
                    pygame.draw.circle(self.screen, (200, 80, 80), pos, 4)
                    
                    # Label court à droite du neurone
                    if i < len(output_short_labels):
                        label_text = self.font.render(output_short_labels[i], True, self.WHITE)
                        # Aligner à droite en calculant la position
                        label_rect = label_text.get_rect()
                        self.screen.blit(label_text, (pos[0] + 40, pos[1] - 8))
                
                # Légende améliorée avec plus d'espace
                legend_y = network_area.bottom + 15  # Plus d'espace
                legend_text = self.small_font.render('Connexions: Jaune=faible  Gris=tres faible  Rouge=fort', True, (200, 200, 200))
                legend_rect = legend_text.get_rect(center=(weights_area.centerx, legend_y))
                self.screen.blit(legend_text, legend_rect)
                
            except Exception as e:
                # En cas d'erreur, afficher un message simple
                error_text = self.small_font.render('Chargement du reseau...', True, self.WHITE)
                error_rect = error_text.get_rect(center=weights_area.center)
                self.screen.blit(error_text, error_rect)
        else:
            # Message d'attente
            wait_text = self.small_font.render('En attente des donnees...', True, self.WHITE)
            text_rect = wait_text.get_rect(center=weights_area.center)
            self.screen.blit(wait_text, text_rect)
    
    def draw_ui(self):
        """Dessine l'interface utilisateur"""
        # Fond
        self.screen.fill(self.BLACK)
        
        # Nombre de parties au-dessus du snake
        parties_text = f"Parties: {self.agent.n_games}"
        parties = self.big_font.render(parties_text, True, self.WHITE)
        parties_rect = parties.get_rect(center=(self.RECORD_WIDTH//2, 30))
        self.screen.blit(parties, parties_rect)
        
        # Stats principales (Record et Moyenne) visibles dans l'enregistrement
        if len(self.plot_scores) > 0:
            mean_score = sum(self.plot_scores) / len(self.plot_scores)
            main_stats_text = f"Record: {self.record}  •  Moyenne: {mean_score:.1f}"
        else:
            main_stats_text = f"Record: {self.record}  •  Score: {self.game.score}"
        
        main_stats = self.big_font.render(main_stats_text, True, (150, 255, 150))
        main_stats_rect = main_stats.get_rect(center=(self.RECORD_WIDTH//2, 55))
        self.screen.blit(main_stats, main_stats_rect)
        
        # Ligne de séparation entre zone d'enregistrement et zone de contrôles
        pygame.draw.line(self.screen, self.GRAY, 
                        (self.RECORD_WIDTH, 0), 
                        (self.RECORD_WIDTH, self.WINDOW_HEIGHT), 2)
        
        # Zone du jeu
        game_surface = self.game.display
        game_rect = pygame.Rect(self.GAME_X, self.GAME_Y, self.GAME_WIDTH, self.GAME_HEIGHT)
        self.screen.blit(game_surface, game_rect)
        
        # Bordure autour du jeu
        pygame.draw.rect(self.screen, self.WHITE, game_rect, 2)
        
        # Panneau de contrôle (zone droite)
        control_y = self.CONTROLS_Y + 250  # En dessous des boutons
        
        # Titre du panneau de contrôle
        control_title = self.font.render('CONTROLES', True, self.WHITE)
        self.screen.blit(control_title, (self.CONTROLS_X, control_y))
        
        # Informations de statut dans la zone de contrôles
        stats_start_y = control_y + 35
        
        # Statistiques de jeu (sans record/moyenne qui sont dans la zone d'enregistrement)
        game_stats = [
            f"Score: {self.game.score}",
            f"Mode: {'RAPIDE' if self.game_speed > 20 else 'NORMAL'}",
            f"Vitesse: {self.game_speed} FPS",
        ]
        
        for i, stat in enumerate(game_stats):
            stat_text = self.small_font.render(stat, True, self.WHITE)
            self.screen.blit(stat_text, (self.CONTROLS_X, stats_start_y + i * 20))
        
        # État de l'entraînement
        training_y = stats_start_y + len(game_stats) * 20 + 20
        training_status = "EN COURS" if self.training else "PAUSE"
        status_color = self.GREEN if self.training else self.RED
        
        status_text = self.small_font.render(f"Entraînement: {training_status}", True, status_color)
        self.screen.blit(status_text, (self.CONTROLS_X, training_y))
        
        # Niveau d'exploration
        exploration_text = self.small_font.render(f"Exploration: {max(0, self.agent.epsilon)}", True, self.WHITE)
        self.screen.blit(exploration_text, (self.CONTROLS_X, training_y + 25))
        
        # Boutons avec design moderne
        for button in self.buttons:
            # Ombre du bouton
            shadow_rect = button['rect'].copy()
            shadow_rect.move_ip(3, 3)
            pygame.draw.rect(self.screen, (50, 50, 50), shadow_rect)
            
            # Bouton principal avec gradient effect
            pygame.draw.rect(self.screen, button['color'], button['rect'])
            
            # Highlight sur le bouton
            highlight_color = tuple(min(255, c + 30) for c in button['color'])
            highlight_rect = pygame.Rect(button['rect'].left + 2, button['rect'].top + 2, 
                                       button['rect'].width - 4, button['rect'].height // 2)
            pygame.draw.rect(self.screen, highlight_color, highlight_rect)
            
            # Bordure
            pygame.draw.rect(self.screen, self.WHITE, button['rect'], 2)
            
            # Texte avec ombre
            shadow_text = self.font.render(button['text'], True, (50, 50, 50))
            text = self.font.render(button['text'], True, self.WHITE)
            
            shadow_rect = shadow_text.get_rect(center=(button['rect'].centerx + 1, button['rect'].centery + 1))
            text_rect = text.get_rect(center=button['rect'].center)
            
            self.screen.blit(shadow_text, shadow_rect)
            self.screen.blit(text, text_rect)
        
        # Graphique moderne
        self.draw_beautiful_graph()
        self.draw_weights_visualization()
    
    def run(self):
        """Boucle principale de l'application"""
        while self.running:
            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clic gauche
                        self.handle_button_click(event.pos)
            
            # Étape d'entraînement
            self.train_step()
            
            # Mise à jour de l'affichage
            self.draw_ui()
            pygame.display.flip()
            
            # Contrôle de la vitesse
            self.clock.tick(self.game_speed)
        
        pygame.quit()

if __name__ == '__main__':
    gui = SnakeAIGUI()
    gui.run() 