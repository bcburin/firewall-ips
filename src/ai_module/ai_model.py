from tqdm import tqdm

import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

  
class Firewall_NN(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.layer1 = nn.Linear(input_dim, 60)
        self.act1 = nn.ReLU()
        self.layer2 = nn.Linear(60, 60)
        self.act2 = nn.ReLU()
        self.layer3 = nn.Linear(60, 60)
        self.act3 = nn.ReLU()
        self.output = nn.Linear(60, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.act1(self.layer1(x))
        x = self.act2(self.layer2(x))
        x = self.act3(self.layer3(x))
        x = self.sigmoid(self.output(x))
        return x


class PytorchAIModel(BaseEstimator, ClassifierMixin):
    def __init__(self, model,criterion=nn.BCELoss(), optimizer=None, epochs=100, batch_size=64, learning_rate=0.001):
        self.model = model
        self.criterion = criterion
        self.epochs = epochs
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.name = "NN"
        if optimizer is None:
            self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        else:
            self.optimizer = optimizer

    def fit(self, X, y):
        self.model.train()
        dataset = TensorDataset(torch.tensor(X.values, dtype=torch.float32), torch.tensor(y, dtype=torch.float32))
        loader = DataLoader(dataset, batch_size=self.batch_size, shuffle=True)
        with tqdm(total=self.epochs * len(loader)) as pbar:
            for epoch in range(self.epochs):
                for inputs, targets in loader:
                    self.optimizer.zero_grad()
                    outputs = self.model(inputs)
                    loss = self.criterion(outputs.flatten(), targets)
                    loss.backward()
                    self.optimizer.step()
                    pbar.update(1)
            return self

    def predict(self, X):
        self.model.eval()
        with torch.no_grad():
            outputs = self.model(torch.tensor(X.values, dtype=torch.float32))
        return (outputs.flatten().numpy() > 0.5).astype(int)

    def predict_proba(self, X):
        self.model.eval()
        with torch.no_grad():
            outputs = self.model(torch.tensor(X.values, dtype=torch.float32))
        probabilities = torch.sigmoid(outputs).numpy()
        return np.hstack([1 - probabilities, probabilities])