# 🐍 Snake AI - Apprentissage par Renforcement

Une implémentation **stable et optimisée** du jeu Snake avec une IA utilisant l'apprentissage par renforcement (Deep Q-Learning) avec un réseau de neurones MLP. L'interface est conçue en format vertical (TikTok) pour créer des vidéos d'entraînement attractives.

> ✅ **Version stable** - Interface unique et fonctionnelle  
> 🚀 **Support GPU/CPU** - Détection automatique  
> 📱 **Format TikTok** - Ratio 9:16 optimisé

## Fonctionnalités

- 🐍 Jeu Snake classique
- 🧠 IA par apprentissage par renforcement (Deep Q-Network)
- 🎛️ Interface utilisateur avec contrôles interactifs
- 📊 Visualisation en temps réel des poids du réseau de neurones
- 📈 Graphiques de progression des scores
- 📱 Format vertical optimisé pour les vidéos TikTok/Instagram
- ⚡ Vitesse ajustable en temps réel

## Architecture

### Réseau de Neurones
- **Entrées (11)**: État du jeu (dangers, direction, position de la nourriture)
- **Couche cachée**: 64 neurones avec activation ReLU
- **Sorties (3)**: Actions possibles (tout droit, droite, gauche)

### Algorithme d'Apprentissage
- **Deep Q-Learning** avec replay memory
- **Exploration vs Exploitation**: Stratégie epsilon-greedy décroissante
- **Optimiseur**: Adam
- **Fonction de perte**: MSE (Mean Squared Error)

## Installation

### 🚀 Installation automatique (recommandée):
```bash
python install.py
```

### Ou installation manuelle:

1. **Cloner le repository:**
```bash
git clone <url-du-repo>
cd Snake
```

2. **Installer les dépendances:**
```bash
pip install -r requirements.txt
```

## Utilisation

### 🚀 Lancement rapide (recommandé):
```bash
python main.py
```

### Ou lancer directement:

**Jeu Snake AI:**
```bash
python gui.py
```

**Test de performance:**
```bash
python test_performance.py
```

**Note GPU/CPU:** L'application détecte automatiquement si un GPU CUDA est disponible. Si oui, elle l'utilisera pour accélérer l'entraînement. Sinon, elle fonctionnera sur CPU.

### Interface Utilisateur

**Zone Supérieure**: Jeu Snake en temps réel
**Zone Contrôles**: 
- `START/STOP`: Démarrer/arrêter l'entraînement
- `RESET`: Réinitialiser l'agent et recommencer
- `+/-`: Ajuster la vitesse du jeu
- Affichage des statistiques (parties, score, record)

**Zone Inférieure**: 
- **Graphique des poids**: Heatmap des poids de la première couche en temps réel
- **Graphique des scores**: Évolution des scores au fil des parties

### Paramètres Ajustables

- **Vitesse du jeu**: 1-50 FPS (boutons +/-)
- **Exploration**: Diminue automatiquement avec le nombre de parties
- **Taille du réseau**: Modifiable dans le code (variable `hidden_size`)

## Structure du Code

```
Snake/
├── install.py              # 🔧 Installation automatique
├── main.py                 # 🚀 Menu de lancement principal
├── gui.py                  # 🎮 Interface de jeu Snake AI (avec zones d'enregistrement)
├── guide_enregistrement.md # 🎬 Guide pour créer des vidéos TikTok
├── check_gpu.py            # 🔍 Vérification GPU/CPU simple
├── test_performance.py     # ⚡ Test de performance détaillé
├── snake_game.py           # 🐍 Logique du jeu Snake
├── agent.py               # 🧠 Agent d'apprentissage par renforcement
├── model.py               # 📊 Réseau de neurones MLP (GPU/CPU)
├── requirements.txt       # 📦 Dépendances
├── CHANGELOG.md          # 📝 Historique des versions
└── README.md             # 📖 Ce fichier
```

### Fichiers Principaux

- **`gui.py`**: Interface graphique principale avec visualisations temps réel
- **`snake_game.py`**: Moteur du jeu Snake avec gestion des états
- **`agent.py`**: Implémentation de l'agent DQN avec mémoire de replay
- **`model.py`**: Définition du réseau de neurones et de l'entraîneur (GPU/CPU)

## Algorithme d'Apprentissage

1. **Observation**: L'agent observe l'état actuel du jeu (11 paramètres)
2. **Action**: Choix d'une action basée sur la politique epsilon-greedy
3. **Récompense**: 
   - +10 pour manger de la nourriture
   - -10 pour mourir
   - 0 sinon
4. **Apprentissage**: Mise à jour des poids via backpropagation
5. **Mémoire**: Stockage des expériences pour l'apprentissage par batch

## État du Jeu (Entrées du Réseau)

### 🧠 Labels des Neurones d'Entrée (11 inputs)

#### **Détection des Dangers (3 inputs) :**
- **DDevant** : Danger si le serpent continue devant lui
- **DDroite** : Danger si le serpent tourne à droite  
- **DGauche** : Danger si le serpent tourne à gauche

#### **Direction Actuelle (4 inputs) :**
- **DirG** : Le serpent va vers la gauche
- **DirD** : Le serpent va vers la droite
- **DirH** : Le serpent va vers le haut
- **DirB** : Le serpent va vers le bas

#### **Position de la Nourriture (4 inputs) :**
- **FG** : Nourriture à gauche du serpent
- **FD** : Nourriture à droite du serpent
- **FH** : Nourriture en haut du serpent
- **FB** : Nourriture en bas du serpent

### 🎯 Labels des Neurones de Sortie (3 outputs)

- **AHaut** : Action aller vers le haut
- **ADroite** : Action aller vers la droite
- **AGauche** : Action aller vers la gauche

### 🔗 Connexions du Réseau

- **Bleu** : Poids faibles (peu d'influence)
- **Gris** : Poids très faibles (mais visibles)
- **Rouge** : Poids forts (influence majeure)

**Note :** Les dangers sont relatifs à la direction du serpent, ce qui rend l'IA plus intelligente car elle apprend des patterns génériques.

## Format TikTok

L'interface est conçue avec un ratio 9:16 (540x960 pixels) pour être parfaitement adaptée aux vidéos verticales des réseaux sociaux.

## 🔍 GPU vs CPU - Questions fréquentes

### "GPU non disponible" - C'est normal !

**90% des utilisateurs n'ont pas de GPU CUDA**, c'est parfaitement normal :

✅ **Votre système fonctionne parfaitement sur CPU**
- Snake AI est optimisé pour CPU
- Performance excellente : ~15,000 inférences/sec
- L'IA apprend normalement
- Aucun matériel supplémentaire requis

### Vérification simple :
```bash
python check_gpu.py
```

### Détection automatique :
L'application s'adapte automatiquement :
- **🚀 GPU NVIDIA** : Accélération 3-5x (rare)
- **💻 CPU Intel/AMD** : Performance optimisée (normal)
- **🎮 GPU intégré** : Fonctionne parfaitement sur CPU

## 🧠 Configuration du Réseau de Neurones

### Changer le nombre de neurones cachés
```python
# Dans gui.py, ligne ~19
self.hidden_size = 128  # ← CHANGEZ ICI (ex: 64, 256, 512)
```

### Visualisation automatique
- **Architecture affichée** : 11→128→3 (correct !)
- **Connexions totales** : 1,792 (11×128 + 128×3)
- **Affichage adaptatif** : Jusqu'à 16 neurones cachés visibles
- **Test facile** : `python test_configurations.py`

**Note technique** : Les dimensions PyTorch sont automatiquement corrigées (format `[out_features, in_features]`).

### 🎯 Configurations Recommandées :

| Configuration | Usage | Performance |
|---------------|--------|-------------|
| `64` | Apprentissage rapide, tests | ⚡ Très rapide |
| `128` | Équilibre optimal (défaut) | ⚖️ Équilibré |
| `256` | Meilleure performance | 🚀 Plus lent mais plus intelligent |
| `512` | Maximum (GPU recommandé) | 🔥 Très lent, très intelligent |

### 📊 Affichage Automatique :

L'interface affiche automatiquement :
- **Titre** : `Reseau 11-128-3` (inputs-hidden-outputs)
- **Visualisation** : Adapte le nombre de neurones affichés
- **Connexions** : Échantillonnage intelligent des poids
- **Console** : `Réseau: 11 → 128 → 3 (affichage: 12 cachés)`

**💡 L'affichage s'adapte automatiquement à votre configuration !**

## Personnalisation

### Modifier la taille du réseau:
```python
# Dans gui.py, ligne ~42
self.hidden_size = 128  # GPU: 256-512, CPU: 64-128
```

### Ajuster les paramètres d'apprentissage:
```python
# Dans agent.py
LR = 0.001          # Taux d'apprentissage
BATCH_SIZE = 1000   # Taille du batch
MAX_MEMORY = 100000 # Taille de la mémoire
```

### Modifier les récompenses:
```python
# Dans snake_game.py, méthode play_step()
reward = 10   # Récompense pour manger
reward = -10  # Pénalité pour mourir
```

## Conseils pour de Bons Résultats

1. **Patience**: L'apprentissage peut prendre 100-200 parties avant de voir des progrès
2. **Vitesse**: Commencer avec une vitesse élevée (20-30) pour un apprentissage rapide
3. **Observation**: Regarder l'évolution des poids pour comprendre l'apprentissage
4. **Reset**: N'hésitez pas à redémarrer si l'agent semble bloqué

## Dépendances

- `pygame==2.5.2`: Moteur de jeu et interface
- `torch==2.1.0`: Réseau de neurones et apprentissage
- `numpy==1.24.3`: Calculs numériques
- `matplotlib==3.7.2`: Visualisations et graphiques

## 🎬 Interface Spéciale Enregistrement

L'interface a été **redesignée pour l'enregistrement de vidéos** :

- **Zone gauche (540px)** : Jeu + Graphiques → **Zone d'enregistrement TikTok**
- **Zone droite (300px)** : Contrôles + Stats → **Hors cadre vidéo**
- **Format parfait** : 540x1000 pixels pour TikTok/Instagram
- **Contrôle temps réel** : Ajustements pendant l'enregistrement

**Voir `guide_enregistrement.md` pour les détails complets !**

L'application est maintenant **parfaite pour créer des vidéos virales** d'IA apprenant à jouer au Snake !

## Licence

Ce projet est open source et libre d'utilisation pour l'éducation et la recherche. 