#!/usr/bin/env python3
"""
Installation automatique pour Snake AI
"""

import subprocess
import sys

def main():
    print("Installation...")
    
    # Installer les dépendances essentielles
    packages = ["pygame-ce", "torch", "numpy", "matplotlib"]
    
    for package in packages:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                         check=True, capture_output=True)
            print(f"OK {package}")
        except subprocess.CalledProcessError:
            print(f"ERREUR {package}")
    
    # Test rapide
    try:
        import torch
        device = "GPU" if torch.cuda.is_available() else "CPU"
        print(f"Device: {device}")
    except ImportError:
        print("Problème d'import")
    
    print("Installation terminée!")

if __name__ == "__main__":
    main() 