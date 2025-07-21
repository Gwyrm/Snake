# 🎬 Guide d'Enregistrement - Snake AI

## 📐 Nouvelle Interface Élargie

L'interface a été redessinée pour faciliter l'enregistrement de vidéos :

```
┌─────────────────────────┬───────────────┐
│                         │               │
│    ZONE D'ENREGISTREMENT │   CONTROLES   │
│        (540px)          │   (300px)     │
│                         │               │
│  🎮 Snake AI            │  [START]      │
│  Parties: 25            │  [RESET]      │
│  Record: 25 • Moyenne: 8.5 │  [NORMAL]  │
│  ┌─────────────────┐    │  [RAPIDE]     │
│  │                 │    │               │
│  │   JEU SNAKE     │    │  CONTROLES    │
│  │                 │    │  Score: 12    │
│  └─────────────────┘    │  Mode: NORMAL │
│                         │  Vitesse: 15  │
│  📊 Evolution Scores    │               │
│  ┌─────────────────┐    │  Entraînement:│
│  │     ╱╲          │    │  EN COURS     │
│  │    ╱  ╲         │    │               │
│  │   ╱    ╲        │    │  Exploration: │
│  └─────────────────┘    │  45           │
│                         │               │
│  🧠 Reseau de Neurones  │               │
│  ┌─────────────────┐    │               │
│  │Danger→●  ●●● ●Haut↑│   │               │
│  │Food← ●   ●●● ●→   │   │               │
│  │  ←   ●●● ●●● ●↓   │   │               │
│  │      Input H Out │   │               │
│  └─Bleu→Rouge──────┘    │               │
│                         │               │
│  Exploration: 45        │               │
│  ████████░░░░░░░░░░░░    │               │
└─────────────────────────┴───────────────┘
```

### Dimensions de la fenêtre : **940x1210** pixels
- **Zone d'enregistrement** : 640x1210 (gauche, pour TikTok) **ÉLARGIE ET ÉPURÉE**
- **Zone de contrôles** : 300x1210 (droite, hors vidéo)
- **Jeu Snake** : 560x560 pixels **AGRANDI** pour meilleure visibilité
- **Réseau de neurones** : 180px de haut, **FOCUS sur la visualisation**
- **Interface minimaliste** : Labels sur le réseau, explications dans le README

## 🎥 Comment Enregistrer

### 1. **Zone d'Enregistrement (Gauche)**
- **Largeur** : 540px (format TikTok parfait)
- **Contenu** : Jeu + Graphiques + **Record & Moyenne visibles**
- **Zone propre** : Aucun bouton de contrôle visible
- **Stats importantes** : Record et moyenne affichés en permanence
- **🆕 Visualisation du réseau** : Réseau de neurones avec couleurs des poids **VISIBLE dans la vidéo !**

### 2. **Zone de Contrôles (Droite)**
- **Largeur** : 300px (hors cadre d'enregistrement)
- **Contenu** : Boutons + Stats détaillées + État
- **Invisible** : Ne sera pas dans la vidéo

## 🎬 Configuration d'Enregistrement

### **Option 1: OBS Studio**
1. Ajouter source "Capture de fenêtre"
2. Sélectionner "Snake AI"
3. **Recadrer** : 
   - Left: 0
   - Right: 300 (pour cacher la zone de contrôles)
   - Top: 0
   - Bottom: 0

### **Option 2: Enregistrement par Zone**
1. Définir une zone de capture de **540x1000 pixels**
2. Positionner depuis le **coin supérieur gauche** de la fenêtre
3. La zone couvrira exactement la partie "enregistrable"

### **Option 3: Bandicam/Fraps**
1. Mode "Zone sélectionnée"
2. Sélectionner la partie gauche de la fenêtre
3. Dimensions automatiques : 540x1000

## ⚙️ Avantages de cette Disposition

### ✅ **Pendant l'Enregistrement**
- **Contrôle total** : Boutons accessibles en temps réel
- **Vidéo propre** : Aucun élément de contrôle visible
- **Ajustements** : Vitesse modifiable sans arrêter l'enregistrement
- **Monitoring** : Stats détaillées toujours visibles

### ✅ **Pour le Rendu Final**
- **Format TikTok** : Ratio personnalisé (640x1210) - Interface épurée et focalisée
- **Référence complète** : Consultez le README.md pour la description détaillée des labels
- **Contenu épuré** : Focus sur le jeu et l'apprentissage
- **Stats visibles** : Record et moyenne toujours affichés dans la vidéo
- **🧠 Réseau visible** : Visualisation complète du réseau neuronal dans la vidéo !
- **Interface optimisée** : Affichage compact, maximum d'informations, minimum d'espace
- **Qualité** : Aucun élément distrayant
- **Professionnel** : Interface clean et moderne

## 🎯 Conseils d'Enregistrement

### **Préparation**
1. Lancer `python gui.py`
2. Positionner la fenêtre pour un accès facile aux contrôles
3. Démarrer l'enregistrement sur la zone gauche
4. Cliquer START dans la zone de droite

### **Pendant l'Enregistrement**
- **Mode NORMAL** : Pour voir l'apprentissage progressif
- **Mode RAPIDE** : Pour accélérer l'entraînement
- **RESET** : Redémarrer si l'IA se bloque
- **Monitoring** : Surveiller les stats à droite

### **Résultat**
- Vidéo de **540x1000 pixels**
- **Format vertical** parfait pour TikTok/Instagram
- **Contenu propre** sans interface de contrôle
- **Apprentissage visible** avec graphiques temps réel

## 🚀 Commandes Rapides

```bash
# Lancer l'interface d'enregistrement
python gui.py

# Vérifier le système
python check_gpu.py

# Test de performance
python test_performance.py
```

**🎬 Prêt pour créer des vidéos d'IA impressionnantes !**

## 🧠 **Nouvelle Fonctionnalité : Visualisation du Réseau de Neurones**

L'interface inclut maintenant une **visualisation en temps réel du réseau de neurones complet** avec des couleurs représentant les poids directement **dans la zone d'enregistrement** !

### **Ce que vous voyez DANS VOS VIDÉOS :**
- **Neurones verts** : Couche d'entrée (11 inputs) **PLUS GROS et plus visibles**
- **Neurones jaunes** : Couche cachée (128 neurones, 16 affichés) **AGRANDIS**
- **Neurones rouges** : Couche de sortie (3 actions) **ENCORE PLUS GROS** 
- **Connexions COMPLÈTES** : 
  - **Bleu → Rouge** : Poids faibles → forts
  - **Gris foncé** : Poids très faibles (mais visibles !)
  - **TOUTES visibles** : Aucune connexion cachée
- **Labels détaillés** : DangerD, FoodG, Haut, etc.
- **Architecture réelle** : 11→128→3 (correctement affichée)
- **Zone agrandie** : 250px de haut pour une visualisation optimale
- **Fond moderne** : Couleurs sombres avec bordures épaisses
- **Temps réel** : Les couleurs changent pendant l'apprentissage !

### 📊 **Architecture Visualisée Complètement :**

```
🟢 INPUTS (11)     🟡 HIDDEN (128)   🔴 OUTPUTS (3)
Danger→  ●─────────● ● ●─────────● Haut ↑
Danger↘  ●─────────● ● ●─────────● Droite →
Danger↖  ●─────────● ● ●─────────● Gauche ↓
←        ●─────────● ● ●
→        ●─────────● ● ●
↑        ●─────────● ● ●
↓        ●─────────● ● ●
Food←    ●─────────● ● ●
Food→    ●─────────● ● ●
Food↑    ●─────────● ● ●
Food↓    ●─────────● ● ●
         1,408 +    384 = 1,792 connexions TOUTES visibles !
```

### 🏷️ **Labels Explicatifs :**

#### **Neurones d'Entrée (11 inputs) :**

**LES 3 DANGERS (relatifs à la direction du serpent) :**
- **DDevant** (danger devant) : Danger si le serpent continue devant lui
- **DDroite** (danger droite) : Danger si le serpent tourne à droite
- **DGauche** (danger gauche) : Danger si le serpent tourne à gauche

**DIRECTION ACTUELLE :**
- **DirG, DirD, DirH, DirB** : Direction où va le serpent (va gauche, va droite, va haut, va bas)

**POSITION DE LA NOURRITURE :**
- **FG, FD, FH, FB** : Où est la nourriture (food gauche, food droite, food haut, food bas)

#### **Neurones de Sortie (3 outputs) :**
- **AHaut** (aller haut) : Aller vers le haut
- **ADroite** (aller droite) : Aller vers la droite  
- **AGauche** (aller gauche) : Aller vers la gauche

### **Comment fonctionnent les dangers :**

**Exemple concret :**
Si le serpent va vers la DROITE :
- **DDevant** = Y a-t-il un obstacle à droite ? (devant lui)
- **DDroite** = Y a-t-il un obstacle en bas ? (tourner à droite)
- **DGauche** = Y a-t-il un obstacle en haut ? (tourner à gauche)

**Intelligence relative :**
L'IA ne raisonne pas en coordonnées absolues mais relativement à sa direction actuelle. C'est plus intelligent car la même situation se répète quelle que soit la direction !

### 🎯 **Avantages RÉVOLUTIONNAIRES pour vos vidéos :**
- **JAMAIS VU** : Visualisation du "cerveau" de l'IA en direct avec labels explicatifs
- **Pédagogique PARFAIT** : "Regardez, l'IA voit un danger à droite !"
- **Engagement maximal** : "Regardez les connexions se renforcer !"
- **Viral garanti** : Contenu que PERSONNE d'autre ne propose
- **Éducatif captivant** : Comprendre l'IA devient facile et visuel
- **🎬 TOUT VISIBLE** : Le réseau complet avec explications dans vos TikToks !

### 🔍 **Interprétation :**
- **Connexions bleues** → Poids faibles, peu d'influence sur la décision
- **Connexions rouges** → Poids forts, influence majeure sur la décision
- **Connexions grises** → Poids très faibles, mais TOUJOURS visibles
- **Changements de couleur** → L'IA apprend et ajuste ses "réflexes"
- **Patterns complets** → Voir TOUTES les connexions et leur évolution
- **Actions finales** → ↑ (haut), → (droite), ↓ (bas/gauche)
- **Réseau COMPLET** → Aucune connexion n'est cachée ou filtrée

### 🎬 **Exemples de Storytelling :**
- *"L'IA detecte un danger devant ! Elle active DevantDroite !"*
- *"La nourriture est à gauche, regardez la connexion FoodG s'allumer !"*
- *"Direction actuelle D se connecte fortement à Droite !"*
- *"L'IA apprend : Devant influence maintenant Haut !"*
- *"Regardez TOUTES les connexions ! Meme les grises comptent !"*
- *"Le reseau COMPLET : rien n'est cache, tout est visible !"*
- *"Connexions faibles en gris, elles vont se renforcer !"*
- *"1,792 connexions qui apprennent en temps reel !"*
- *"Danger devant ! Le serpent doit choisir droite ou gauche !"*
- *"Intelligence relative : l'IA pense devant, droite, gauche !"*

**💡 Parfait pour créer des vidéos éducatives sur l'intelligence artificielle !** 