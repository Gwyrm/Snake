import torch
import time
import numpy as np
from model import Linear_QNet

def test_performance():
    """Test des performances GPU vs CPU"""
    
    print("Test de performance")
    
    # Vérification CUDA
    cuda_available = torch.cuda.is_available()
    device = "GPU" if cuda_available else "CPU"
    print(f"Device: {device}")
    
    # Paramètres du test
    input_size = 11
    hidden_size = 256
    output_size = 3
    num_iterations = 1000
    batch_size = 32
    
    # Test sur CPU
    print(f"\n🔄 Test CPU ({num_iterations} itérations)")
    model_cpu = Linear_QNet(input_size, hidden_size, output_size)
    model_cpu.device = torch.device("cpu")
    model_cpu.to(model_cpu.device)
    
    # Données de test
    test_input = torch.randn(batch_size, input_size)
    
    start_time = time.time()
    for i in range(num_iterations):
        with torch.no_grad():
            output = model_cpu(test_input)
    cpu_time = time.time() - start_time
    
    print(f"Temps CPU: {cpu_time:.3f}s")
    print(f"Inférences/sec: {num_iterations/cpu_time:.0f}")
    
    # Test sur GPU (si disponible)
    if cuda_available:
        print(f"\n🚀 Test GPU ({num_iterations} itérations)")
        model_gpu = Linear_QNet(input_size, hidden_size, output_size)
        # Le modèle va automatiquement sur GPU grâce à notre code
        
        # Données de test sur GPU
        test_input_gpu = test_input.to(model_gpu.device)
        
        # Warm-up
        for _ in range(10):
            with torch.no_grad():
                _ = model_gpu(test_input_gpu)
        torch.cuda.synchronize()
        
        start_time = time.time()
        for i in range(num_iterations):
            with torch.no_grad():
                output = model_gpu(test_input_gpu)
        torch.cuda.synchronize()
        gpu_time = time.time() - start_time
        
        print(f"Temps GPU: {gpu_time:.3f}s")
        print(f"Inférences/sec: {num_iterations/gpu_time:.0f}")
        print(f"Accélération: {cpu_time/gpu_time:.1f}x")
        
        # Mémoire GPU utilisée
        memory_used = torch.cuda.memory_allocated() / 1024**2
        print(f"Mémoire GPU utilisée: {memory_used:.1f} MB")
    
    else:
        print("\n💻 Test de performance sur CPU...")
    
    print(f"\nPerformance: {num_iterations/cpu_time:.0f} inférences/sec")
    print("Système prêt !")

if __name__ == "__main__":
    test_performance() 