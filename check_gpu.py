#!/usr/bin/env python3
"""
Vérification GPU/CPU pour Snake AI
"""

import torch
import platform

def main():
    print("Vérification système")
    
    # Test CUDA
    cuda_available = torch.cuda.is_available()
    print(f"CUDA: {'DISPONIBLE' if cuda_available else 'NON DISPONIBLE'}")
    
    if cuda_available:
        print("\nGPU NVIDIA détecté !")
        print(f"   GPU: {torch.cuda.get_device_name(0)}")
        print(f"   VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
        print("   Snake AI utilisera l'accélération GPU")
        print("   Performance: 3-5x plus rapide")
    else:
        print("\nPas de GPU CUDA - C'est normal !")
        print("   Raisons courantes:")
        print("     • GPU Intel HD/AMD (pas CUDA)")
        print("     • Pas de GPU NVIDIA")
        print("     • CUDA non installé")
        print("     • Ordinateur portable/bureau standard")
        
        print(f"\nPas de problème ! Votre CPU est parfait:")
        print("   Snake AI fonctionne excellemment sur CPU")
        print("   L'IA apprendra normalement")
        print("   Jeu fluide et responsive")
        print("   Aucun achat de matériel nécessaire")
    
    print("\nSystème prêt pour Snake AI !")

if __name__ == "__main__":
    main() 