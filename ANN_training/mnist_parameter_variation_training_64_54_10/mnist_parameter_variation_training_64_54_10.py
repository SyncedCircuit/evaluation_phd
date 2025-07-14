import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from sklearn import datasets
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.base import BaseEstimator, ClassifierMixin
from torch.utils.data import DataLoader, TensorDataset

# Constants
num_states = 100
asymmetric_ratio = 0.06
retention_rate = 0.98
dynamic_range = 400
G_max = 1e-5
G_min = 2e-6
v = torch.tensor(0.3, dtype=torch.float32)  # Ensure v is a Tensor

# Define the neural network
class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.fc1 = nn.Linear(64, 54 * num_states)
        self.fc2 = nn.Linear(54 * num_states, 54 * num_states)
        self.fc3 = nn.Linear(54 * num_states, 10)
        self.activation = nn.Tanh()

    def forward(self, x):
        x = self.activation(self.fc1(x))
        x = self.activation(self.fc2(x))
        x = self.fc3(x)
        return x

# Custom PyTorch classifier
class PyTorchClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self, model, criterion, optimizer, num_epochs=50, use_custom_update=False):
        self.model = model
        self.criterion = criterion
        self.optimizer = optimizer
        self.num_epochs = num_epochs
        self.use_custom_update = use_custom_update
        self.test_accuracies = []

    def fit(self, X_train, y_train, X_test, y_test):
        train_dataset = TensorDataset(
            torch.tensor(X_train, dtype=torch.float32),
            torch.tensor(y_train, dtype=torch.long)
        )
        train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)

        X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
        y_test_tensor = torch.tensor(y_test, dtype=torch.long)

        self.model.apply(self._reset_weights)

        for epoch in range(self.num_epochs):
            running_loss = 0.0
            for inputs, labels in train_loader:
                self.optimizer.zero_grad()
                outputs = self.model(inputs)
                loss = self.criterion(outputs, labels)
                loss.backward()

                if self.use_custom_update:
                    for param in self.model.parameters():
                        if param.grad is not None:
                            G = param.data
                            dG_target = asymmetric_ratio * param.grad.data
                            d = dG_target / (G_max - G_min)
                            exp_v = torch.exp(-v)
                            dG = (((G_max - G_min) / (1 - exp_v)) + G_min - G) * (1 - torch.exp(-v * d))
                            param.data += dG
                            param.data *= retention_rate
                            param.data = torch.clamp(param.data, -dynamic_range, dynamic_range)

                self.optimizer.step()
                running_loss += loss.item()

            with torch.no_grad():
                self.model.eval()
                outputs_test = self.model(X_test_tensor)
                _, predicted_test = torch.max(outputs_test, 1)
                correct_predictions = (predicted_test == y_test_tensor).sum().item()
                accuracy = correct_predictions / y_test_tensor.size(0)
                self.test_accuracies.append(accuracy)
                print(f"Epoch {epoch + 1}, Loss: {running_loss:.4f}, Accuracy: {accuracy:.4f}")

        return np.mean(self.test_accuracies)

    def _reset_weights(self, layer):
        if isinstance(layer, nn.Linear):
            nn.init.normal_(layer.weight, mean=0, std=0.01)
            nn.init.constant_(layer.bias, 0)

# Load dataset
digits = datasets.load_digits()
X_data = digits.data
y_data = digits.target

scaler = StandardScaler()
X_data = scaler.fit_transform(X_data)

criterion = nn.CrossEntropyLoss()

kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
custom_fold_accuracies, baseline_fold_accuracies = [], []

# Cross-validation loop
for fold, (train_index, test_index) in enumerate(kf.split(X_data, y_data), 1):
    X_train, X_test = X_data[train_index], X_data[test_index]
    y_train, y_test = y_data[train_index], y_data[test_index]

    print(f"\nFold {fold} - Custom Synaptic Weight Update Model")
    neural_net_custom = NeuralNetwork()
    optimizer_custom = optim.SGD(neural_net_custom.parameters(), lr=0.001, momentum=0.9)
    pytorch_classifier_custom = PyTorchClassifier(
        model=neural_net_custom,
        criterion=criterion,
        optimizer=optimizer_custom,
        num_epochs=50,
        use_custom_update=True
    )
    custom_accuracy = pytorch_classifier_custom.fit(X_train, y_train, X_test, y_test)
    custom_fold_accuracies.append(custom_accuracy)

    print(f"\nFold {fold} - Baseline Model")
    neural_net_baseline = NeuralNetwork()
    optimizer_baseline = optim.SGD(neural_net_baseline.parameters(), lr=0.001, momentum=0.9)
    pytorch_classifier_baseline = PyTorchClassifier(
        model=neural_net_baseline,
        criterion=criterion,
        optimizer=optimizer_baseline,
        num_epochs=50,
        use_custom_update=False
    )
    baseline_accuracy = pytorch_classifier_baseline.fit(X_train, y_train, X_test, y_test)
    baseline_fold_accuracies.append(baseline_accuracy)

# Compare results
print(f"\nCustom Model Mean Accuracy: {np.mean(custom_fold_accuracies):.4f} ± {np.std(custom_fold_accuracies):.4f}")
print(f"Baseline Model Mean Accuracy: {np.mean(baseline_fold_accuracies):.4f} ± {np.std(baseline_fold_accuracies):.4f}")
