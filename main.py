#!/usr/bin/env python3
"""
Script de lancement principal pour Snake AI
Détecte automatiquement les capacités du système et lance la version optimale
"""

import sys
import subprocess
import torch

def main():
    print("Snake AI")
    
    # Détection simple
    cuda_available = torch.cuda.is_available()
    device = "GPU" if cuda_available else "CPU"
    print(f"Device: {device}")
    
    # Menu
    print("\nMenu:")
    print("1. Jouer")
    print("2. Vérifier système") 
    print("3. Test performance")
    print("4. Quitter")
    
    while True:
        try:
            choice = input("\nChoix (1-4): ").strip()
            
            if choice == "1":
                subprocess.run([sys.executable, "gui.py"])
                break
                
            elif choice == "2":
                subprocess.run([sys.executable, "check_gpu.py"])
                input("\n↵ Entrée pour continuer...")
                continue
                
            elif choice == "3":
                subprocess.run([sys.executable, "test_performance.py"])
                input("\n↵ Entrée pour continuer...")
                continue
                
            elif choice == "4":
                break
                
            else:
                print("❌ Choix invalide")
                
        except KeyboardInterrupt:
            break
        except Exception:
            break

if __name__ == "__main__":
    main() 