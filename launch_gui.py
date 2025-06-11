#!/usr/bin/env python3
"""
🎮 SNAKE AI - LANCEMENT GUI UNIVERSEL
====================================

Script de lancement rapide pour entraîner différents agents Snake avec interface graphique
"""

import sys
import os
from universal_gui_trainer import UniversalGUITrainer, list_available_agents, train_agent

def main():
    print("🐍 SNAKE AI - LANCEMENT GUI")
    print("=" * 50)
    
    if len(sys.argv) == 1:
        # Mode interactif
        print("Choisissez un agent à entraîner :")
        print()
        
        agents = list_available_agents()
        print()
        
        if not agents:
            print("❌ Aucun agent trouvé !")
            return
        
        # Menu interactif
        for i, agent in enumerate(agents, 1):
            print(f"  {i}. {agent}")
        print("  0. Quitter")
        
        try:
            choice = int(input("\nVotre choix (1-{}): ".format(len(agents))))
            if choice == 0:
                return
            elif 1 <= choice <= len(agents):
                agent_name = agents[choice - 1]
            else:
                print("❌ Choix invalide !")
                return
        except ValueError:
            print("❌ Veuillez entrer un nombre !")
            return
    
    elif len(sys.argv) == 2:
        # Mode direct
        agent_name = sys.argv[1]
    
    else:
        print("Usage:")
        print("  python launch_gui.py              # Mode interactif")
        print("  python launch_gui.py <agent>      # Mode direct")
        return
    
    # Lancement de l'entraînement
    print(f"\n🚀 Lancement de l'entraînement pour {agent_name}...")
    print("   (Ctrl+C pour arrêter)")
    print()
    
    try:
        train_agent(agent_name, gui=True)
    except KeyboardInterrupt:
        print("\n\n⏹️  Entraînement interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur : {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main() 