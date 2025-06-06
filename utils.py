#!/usr/bin/env python3
"""
🛠️ UTILS - Utilitaires pour le projet Snake AI
==============================================

Script d'utilitaires pour maintenir et nettoyer le projet
"""

import os
import sys
import shutil
import glob

def clean_cache():
    """Nettoie les fichiers de cache Python"""
    print("🧹 Nettoyage du cache Python...")
    
    # Supprimer __pycache__
    for root, dirs, files in os.walk('.'):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                cache_path = os.path.join(root, dir_name)
                print(f"   Suppression: {cache_path}")
                shutil.rmtree(cache_path, ignore_errors=True)
    
    # Supprimer les fichiers .pyc
    pyc_files = glob.glob('**/*.pyc', recursive=True)
    for pyc_file in pyc_files:
        print(f"   Suppression: {pyc_file}")
        os.remove(pyc_file)
    
    print("✅ Cache Python nettoyé")

def clean_models():
    """Nettoie les anciens modèles"""
    print("🧹 Nettoyage des modèles...")
    
    model_dir = 'model'
    if os.path.exists(model_dir):
        models = os.listdir(model_dir)
        if models:
            print(f"   Modèles trouvés: {', '.join(models)}")
            response = input("   Voulez-vous supprimer tous les modèles ? (y/N): ")
            if response.lower() == 'y':
                shutil.rmtree(model_dir)
                os.makedirs(model_dir, exist_ok=True)
                print("✅ Modèles supprimés")
            else:
                print("   Modèles conservés")
        else:
            print("   Aucun modèle à nettoyer")
    else:
        print("   Dossier model/ introuvable")

def clean_plots():
    """Nettoie les graphiques générés"""
    print("🧹 Nettoyage des graphiques...")
    
    plot_files = glob.glob('*.png') + glob.glob('*.jpg') + glob.glob('*.svg')
    if plot_files:
        print(f"   Graphiques trouvés: {', '.join(plot_files)}")
        response = input("   Voulez-vous supprimer les graphiques ? (y/N): ")
        if response.lower() == 'y':
            for plot_file in plot_files:
                os.remove(plot_file)
                print(f"   Suppression: {plot_file}")
            print("✅ Graphiques supprimés")
        else:
            print("   Graphiques conservés")
    else:
        print("   Aucun graphique à nettoyer")

def show_project_stats():
    """Affiche les statistiques du projet"""
    print("📊 STATISTIQUES DU PROJET")
    print("=" * 40)
    
    # Compter les fichiers Python
    py_files = glob.glob('*.py')
    print(f"📝 Fichiers Python: {len(py_files)}")
    for py_file in sorted(py_files):
        with open(py_file, 'r', encoding='utf-8') as f:
            lines = len(f.readlines())
        print(f"   • {py_file}: {lines} lignes")
    
    # Compter les modèles
    model_dir = 'model'
    if os.path.exists(model_dir):
        models = os.listdir(model_dir)
        print(f"\n🧠 Modèles sauvegardés: {len(models)}")
        for model in sorted(models):
            model_path = os.path.join(model_dir, model)
            size = os.path.getsize(model_path) / 1024  # KB
            print(f"   • {model}: {size:.1f} KB")
    
    # Taille totale du projet
    total_size = 0
    for root, dirs, files in os.walk('.'):
        if 'snake_env' in root or '.git' in root:
            continue
        for file in files:
            file_path = os.path.join(root, file)
            total_size += os.path.getsize(file_path)
    
    print(f"\n💾 Taille totale: {total_size/1024:.1f} KB")

def list_agents():
    """Liste les agents disponibles avec leurs caractéristiques"""
    print("🤖 AGENTS DISPONIBLES")
    print("=" * 40)
    
    agents_info = [
        ('agent.py', 'Agent', 'Agent original DQN simple'),
        ('improved_agent.py', 'ImprovedAgent', 'Agent avec détection de pièges'),
        ('enhanced_training.py', 'EnhancedAgent', 'Agent optimisé haute performance')
    ]
    
    for file, class_name, description in agents_info:
        if os.path.exists(file):
            print(f"✅ {class_name}")
            print(f"   📄 Fichier: {file}")
            print(f"   📋 Description: {description}")
            
            # Analyser les fonctionnalités
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    features = []
                    if 'count_free_spaces' in content:
                        features.append('Flood Fill')
                    if 'gamma' in content and '0.9' in content:
                        features.append('Long-term Planning')
                    if 'epsilon' in content:
                        features.append('ε-greedy')
                    
                    if features:
                        print(f"   ⚡ Fonctionnalités: {', '.join(features)}")
            except:
                pass
            print()
        else:
            print(f"❌ {class_name} (fichier manquant: {file})")

def main():
    if len(sys.argv) == 1:
        print("🛠️ UTILS SNAKE AI")
        print("=" * 30)
        print("Commandes disponibles:")
        print("  clean-cache    - Nettoie le cache Python")
        print("  clean-models   - Nettoie les modèles")
        print("  clean-plots    - Nettoie les graphiques")
        print("  clean-all      - Nettoie tout")
        print("  stats          - Affiche les statistiques")
        print("  list-agents    - Liste les agents")
        print()
        print("Usage: python utils.py <commande>")
        return
    
    command = sys.argv[1]
    
    if command == 'clean-cache':
        clean_cache()
    elif command == 'clean-models':
        clean_models()
    elif command == 'clean-plots':
        clean_plots()
    elif command == 'clean-all':
        clean_cache()
        clean_models()
        clean_plots()
        print("🎉 Nettoyage complet terminé !")
    elif command == 'stats':
        show_project_stats()
    elif command == 'list-agents':
        list_agents()
    else:
        print(f"❌ Commande inconnue: {command}")
        print("Utilisez 'python utils.py' pour voir les commandes disponibles")

if __name__ == '__main__':
    main() 