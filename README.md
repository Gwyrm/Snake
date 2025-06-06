# Snake AI - Apprentissage par Renforcement avec PyTorch

Ce projet implémente un jeu Snake contrôlé par une IA utilisant l'apprentissage par renforcement (Deep Q-Learning) avec PyTorch.

## 🎮 Fonctionnalités

- **Jeu Snake complet** avec interface graphique PyGame
- **Agent d'IA** utilisant Deep Q-Network (DQN)
- **Apprentissage par renforcement** avec exploration/exploitation
- **Visualisation en temps réel** des performances
- **Sauvegarde/chargement** des modèles entraînés

## 📁 Structure du projet

```
├── snake_game.py    # Logique du jeu Snake
├── agent.py         # Agent d'IA et boucle d'entraînement
├── model.py         # Réseau de neurones DQN
├── helper.py        # Fonctions de visualisation
├── play.py          # Script pour jouer avec un modèle entraîné
├── requirements.txt # Dépendances
└── model/          # Dossier pour sauvegarder les modèles (créé automatiquement)
```

## 🚀 Installation

1. **Cloner le repository**
```bash
git clone <url_du_repo>
cd Snake
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

## 🎯 Utilisation

### Entraîner l'IA

Pour commencer l'entraînement de l'agent IA :

```bash
python agent.py
```

L'agent va :
- Jouer de nombreuses parties
- Apprendre de ses erreurs
- Améliorer progressivement ses performances
- Sauvegarder automatiquement le meilleur modèle

### Jouer avec l'IA entraînée

Pour voir l'IA jouer avec un modèle pré-entraîné :

```bash
python play.py
```

## 🧠 Comment ça fonctionne

### Environnement
- **Espace d'état** : 11 variables binaires décrivant l'environnement
  - Danger immédiat (tout droit, droite, gauche)
  - Direction actuelle (4 directions)
  - Position relative de la nourriture (4 directions)

- **Actions** : 3 actions possibles
  - Continuer tout droit
  - Tourner à droite
  - Tourner à gauche

- **Récompenses** :
  - +10 pour manger de la nourriture
  - -10 pour mourir (collision)
  - 0 pour les autres mouvements

### Architecture du réseau
- **Couche d'entrée** : 11 neurones (état du jeu)
- **Couche cachée** : 256 neurones avec activation ReLU
- **Couche de sortie** : 3 neurones (Q-values pour chaque action)

### Algorithme d'apprentissage
- **Deep Q-Learning** avec replay buffer
- **Epsilon-greedy** pour l'exploration
- **Experience replay** pour stabiliser l'apprentissage
- **Target network** implicite via mise à jour des poids

## 📊 Paramètres d'entraînement

- **Learning rate** : 0.001
- **Gamma (discount factor)** : 0.9
- **Epsilon decay** : 80 - nombre_de_jeux
- **Batch size** : 1000
- **Memory size** : 100,000

## 🔧 Personnalisation

Vous pouvez modifier les paramètres dans `agent.py` :

```python
MAX_MEMORY = 100_000  # Taille du replay buffer
BATCH_SIZE = 1000     # Taille des mini-batches
LR = 0.001           # Taux d'apprentissage
```

Ou ajuster l'architecture du réseau dans `model.py` :

```python
self.model = Linear_QNet(11, 256, 3)  # input, hidden, output
```

## 📈 Résultats attendus

L'agent devrait :
- Commencer par des scores très bas (0-2)
- Progressivement améliorer ses performances
- Atteindre des scores de 10+ après quelques centaines de jeux
- Potentiellement atteindre 20+ avec un entraînement prolongé

## 🎮 Contrôles

Pendant l'entraînement ou le jeu :
- Fermez la fenêtre pour arrêter le programme
- Les scores et statistiques s'affichent dans la console

## 🚨 Dépannage

**Erreur de police** : Si vous obtenez une erreur avec `arial.ttf`, modifiez dans `snake_game.py` :
```python
font = pygame.font.Font(None, 25)  # Utilise la police par défaut
```

**Erreur d'affichage** : Si les graphiques ne s'affichent pas, commentez les lignes de visualisation dans `helper.py`.

## 🎯 Améliorations possibles

- Ajouter des convolutions pour traiter l'image directement
- Implémenter Double DQN ou Dueling DQN
- Ajouter plus de features à l'espace d'état
- Optimiser les hyperparamètres
- Ajouter un mode multijoueur

---

🎉 **Amusez-vous bien avec votre Snake IA !**