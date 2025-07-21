import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import warnings

# Supprimer les warnings verbeux
warnings.filterwarnings("ignore", category=UserWarning)

class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        # Détection automatique du device (GPU si disponible, sinon CPU)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)
        
        # Déplacer le modèle sur le device approprié
        self.to(self.device)
        
    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x
    
    def save(self, file_name='model.pth'):
        torch.save(self.state_dict(), file_name)
    
    def get_weights(self):
        """Retourne les poids de la première couche pour visualisation"""
        return self.linear1.weight.data.cpu().numpy()
    
    def get_biases(self):
        """Retourne les biais de la première couche pour visualisation"""
        return self.linear1.bias.data.cpu().numpy()
    
    def get_layer2_weights(self):
        """Retourne les poids de la deuxième couche pour visualisation"""
        return self.linear2.weight.data.cpu().numpy()
    
    def get_layer2_biases(self):
        """Retourne les biais de la deuxième couche pour visualisation"""
        return self.linear2.bias.data.cpu().numpy()

class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.device = model.device  # Utilise le même device que le modèle
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        # Créer les tensors et les déplacer sur le bon device
        state = torch.tensor(state, dtype=torch.float).to(self.device)
        next_state = torch.tensor(next_state, dtype=torch.float).to(self.device)
        action = torch.tensor(action, dtype=torch.long).to(self.device)
        reward = torch.tensor(reward, dtype=torch.float).to(self.device)
        # (n, x)

        if len(state.shape) == 1:
            # (1, x)
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        # 1: predicted Q values with current state
        pred = self.model(state)

        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))

            target[idx][torch.argmax(action[idx]).item()] = Q_new
    
        # 2: Q_new = r + y * max(next_predicted Q value) -> only do this if not done
        # pred.clone()
        # preds[argmax(action)] = Q_new
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimizer.step() 