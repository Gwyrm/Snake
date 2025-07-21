#!/usr/bin/env python3
"""
Test des différentes configurations de réseau de neurones
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent import Agent
import numpy as np

def test_network_config(hidden_size):
    """Teste une configuration de reseau"""
    print(f"\nTest reseau avec {hidden_size} neurones caches:")
    
    try:
        # Créer l'agent avec la configuration
        agent = Agent(hidden_size=hidden_size)
        
        # Récupérer les dimensions
        weights1 = agent.model.get_weights()
        weights2 = agent.model.get_layer2_weights()
        
        # ATTENTION: PyTorch stocke les poids en (out_features, in_features)
        input_size = weights1.shape[1]  # in_features de linear1
        hidden_real = weights1.shape[0]  # out_features de linear1 
        output_size = weights2.shape[0]  # out_features de linear2
        
        print(f"   Architecture: {input_size} - {hidden_real} - {output_size}")
        print(f"   Parametres totaux: {np.prod(weights1.shape) + np.prod(weights2.shape):,}")
        print(f"   Affichage adaptatif: {min(16, max(8, hidden_real // 8))} neurones caches visibles")
        print(f"   Configuration valide !")
        
        return True
        
    except Exception as e:
        print(f"   Erreur: {e}")
        return False

def main():
    """Test des configurations recommandees"""
    print("Test des Configurations de Reseau de Neurones")
    print("=" * 50)
    
    configurations = [
        (64, "Apprentissage rapide"),
        (128, "Equilibre optimal (defaut)"),
        (256, "Meilleure performance"),
        (512, "Maximum")
    ]
    
    results = []
    
    for hidden_size, description in configurations:
        print(f"\n{description}")
        success = test_network_config(hidden_size)
        results.append((hidden_size, success))
    
    print(f"\nResume des tests:")
    print("-" * 30)
    for hidden_size, success in results:
        status = "OK" if success else "ERREUR"
        print(f"   {hidden_size:3d} neurones: {status}")
    
    print(f"\nPour changer la configuration:")
    print(f"   Modifiez self.hidden_size dans gui.py")
    print(f"   L'affichage s'adaptera automatiquement !")

if __name__ == "__main__":
    main() 