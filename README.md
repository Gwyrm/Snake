# 🐍 Snake AI - Apprentissage par Renforcement avec PyTorch

Un projet d'intelligence artificielle pour créer des agents Snake qui apprennent à jouer grâce au **Deep Q-Learning** avec PyTorch et interface graphique PyGame.

## 🎯 Fonctionnalités

- 🧠 **3 agents différents** avec complexité croissante
- 🎮 **Interface graphique** en temps réel avec PyGame
- 📊 **Visualisation** des performances en temps réel
- 🔄 **Système universel** pour entraîner n'importe quel agent
- 🛠️ **Utilitaires** de gestion et nettoyage du projet

## 🚀 Installation

```bash
# Cloner le projet
git clone <votre-repo>
cd Snake

# Créer un environnement virtuel
python -m venv snake_env
source snake_env/bin/activate  # Linux/Mac
# ou snake_env\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
```

## 🤖 Les Agents

### 1. Agent Original (`agent.py`)
- **Architecture**: 11→256→3 neurones
- **Fonctionnalités**: DQN basique, ε-greedy
- **Performance**: Rapide à entraîner, scores élevés mais instables

### 2. Agent Amélioré (`improved_agent.py`)
- **Architecture**: 16→256→3 neurones
- **Fonctionnalités**: Détection de pièges (Flood Fill), récompenses optimisées
- **Performance**: Plus stable, évite mieux l'auto-collision

### 3. Agent Enhanced (`enhanced_training.py`)
- **Architecture**: 16→512→3 neurones
- **Fonctionnalités**: Planification long-terme (γ=0.95), architecture optimisée
- **Performance**: Meilleur compromis stabilité/performance

## 🎮 Utilisation

### Lancement Rapide (Interface Graphique)

```bash
# Mode interactif - choisir l'agent
python launch_gui.py

# Mode direct - spécifier l'agent
python launch_gui.py Agent          # Agent original
python launch_gui.py ImprovedAgent  # Agent amélioré
python launch_gui.py EnhancedAgent  # Agent enhanced
```

### Système Universel (Avancé)

```python
from universal_gui_trainer import UniversalGUITrainer

# Entraîner n'importe quel agent
trainer = UniversalGUITrainer('Agent')
trainer.train_with_gui()

# Test rapide sans GUI
trainer.quick_test(num_games=10)
```

### Jouer avec un Modèle Pré-entraîné

```bash
python play.py
```

## 🛠️ Utilitaires

```bash
# Voir les agents disponibles
python utils.py list-agents

# Statistiques du projet
python utils.py stats

# Nettoyage
python utils.py clean-cache    # Cache Python
python utils.py clean-models   # Modèles sauvegardés
python utils.py clean-all      # Nettoyage complet
```

## 📁 Structure du Projet

```
Snake/
├── 🤖 Agents
│   ├── agent.py              # Agent original
│   ├── improved_agent.py     # Agent amélioré
│   └── enhanced_training.py  # Agent enhanced
├── 🎮 Interface & Jeu
│   ├── snake_game.py         # Moteur de jeu PyGame
│   ├── launch_gui.py         # Lancement GUI simple
│   └── universal_gui_trainer.py # Système universel
├── 🧠 Modèle IA
│   ├── model.py              # Réseau neuronal
│   └── helper.py             # Visualisation
├── 🎯 Utilisation
│   ├── play.py               # Jouer avec modèle
│   └── utils.py              # Utilitaires projet
├── 📄 Documentation
│   ├── README.md             # Ce fichier
│   └── IMPROVEMENTS_SUMMARY.md # Détails techniques
├── 📦 Configuration
│   └── requirements.txt      # Dépendances
└── 💾 Modèles (généré)
    └── model/                # Modèles sauvegardés
```

## 🔧 Technologies

- **🐍 Python 3.8+**
- **🔥 PyTorch** - Apprentissage profond
- **🎮 PyGame** - Interface graphique
- **📊 Matplotlib** - Visualisation
- **🔢 NumPy** - Calculs numériques

## 🎯 Algorithme

Le projet utilise le **Deep Q-Learning (DQN)** :

1. **État** : Position snake, nourriture, dangers (11-16 variables)
2. **Actions** : Tout droit, tourner gauche/droite
3. **Récompenses** : +10 nourriture, -10 collision, bonus optimisés
4. **Réseau** : Fully connected layers avec ReLU
5. **Entraînement** : Experience replay + target network

## 📈 Résultats

| Agent | Score Moyen | Record | Stabilité | Fonctionnalités |
|-------|-------------|---------|-----------|-----------------|
| Original | 33.7 | 67 | ±12.3 | DQN basique |
| Amélioré | 6.9 | 19 | ±4.1 | + Flood Fill |
| Enhanced | ~40 | 60+ | Optimisé | + Long-term Planning |

## 🚀 Fonctionnalités Avancées

### Détection de Pièges (Flood Fill)
Algorithme qui analyse l'espace libre autour du snake pour éviter de se coincer.

### Système de Récompenses Intelligent
- Récompenses progressives selon la taille
- Bonus pour se rapprocher de la nourriture
- Pénalités douces pour encourager l'exploration

### Interface Universelle
Le système peut automatiquement détecter et utiliser n'importe quelle classe d'agent compatible.

## 🎮 Contrôles pendant l'Entraînement

- **Fermer la fenêtre** : Arrêter l'entraînement
- **Ctrl+C** : Arrêt propre dans le terminal
- **Graphiques** : Mise à jour automatique des performances

## 🔄 Améliorations Futures

- 🌐 **Réseau convolutionnel** pour vision spatiale
- 🎯 **A3C/PPO** pour exploration améliorée
- 🏆 **Tournois** entre agents
- 📱 **Interface web** avec Flask/Streamlit
- 🎨 **Thèmes visuels** personnalisables

## 🤝 Contribution

Les contributions sont les bienvenues ! Voir `IMPROVEMENTS_SUMMARY.md` pour les détails techniques.

## 📄 Licence

MIT License - voir LICENSE pour les détails.

---

**🎮 Amusez-vous bien avec votre Snake AI !** 🐍🤖