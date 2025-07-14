import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from torchvision.datasets import MNIST
from torchvision.transforms import ToTensor
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import confusion_matrix
from sklearn.base import BaseEstimator, ClassifierMixin

# -----------------------------------
# 1) Load & preprocess 28×28 MNIST data
# -----------------------------------
mnist_train = MNIST(root='./data', train=True, download=True, transform=ToTensor())
mnist_test  = MNIST(root='./data', train=False, download=True, transform=ToTensor())

# Flatten images to vectors of length 784 and normalize to [0,1]
X_train = mnist_train.data.view(-1, 28*28).float() / 255.0
y_train = mnist_train.targets
X_test  = mnist_test.data.view(-1, 28*28).float() / 255.0
y_test  = mnist_test.targets

# Combine for cross-validation
X_all = torch.cat([X_train, X_test]).numpy()
y_all = torch.cat([y_train, y_test]).numpy()

# -----------------------------------
# 2) Define the network architecture
# -----------------------------------
class SimpleMLP(nn.Module):
    def __init__(self, input_dim=784, hidden_dim=100, output_dim=10):
        super(SimpleMLP, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = self.relu(self.fc1(x))
        return self.fc2(x)

# -----------------------------------
# 3) Sklearn-compatible wrapper
# -----------------------------------
class PyTorchNNWrapper(BaseEstimator, ClassifierMixin):
    def __init__(self,
                 input_dim=784,
                 hidden_dim=100,
                 output_dim=10,
                 lr_pos=0.1,
                 lr_neg=0.103,        # made closer for ~3% asymmetry
                 retention=1e-5,      # much lower retention drift
                 W_min=0.1,
                 W_max=0.51,
                 quantize=True,       # allow toggling quantization
                 retain=True,         # allow toggling retention
                 epochs=50,
                 batch_size=64,
                 device=None,
                 random_state=None):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        self.lr_pos = lr_pos
        self.lr_neg = lr_neg
        self.retention = retention
        self.W_min = W_min
        self.W_max = W_max
        self.quantize = quantize
        self.retain = retain
        self.epochs = epochs
        self.batch_size = batch_size
        self.device = device
        self.random_state = random_state
        self.model = None

    def fit(self, X, y, X_val=None, y_val=None):
        # reproducibility
        if self.random_state is not None:
            torch.manual_seed(self.random_state)
            np.random.seed(self.random_state)

        device = torch.device(self.device if self.device
                              else ('cuda' if torch.cuda.is_available() else 'cpu'))

        self.model = SimpleMLP(self.input_dim, self.hidden_dim, self.output_dim).to(device)
        criterion = nn.CrossEntropyLoss()

        # Standard SGD optimizer to compare against manual updates
        optimizer = optim.SGD(self.model.parameters(), lr=self.lr_pos)  # start with lr_pos

        # Prepare data
        X_tensor = torch.tensor(X, dtype=torch.float32)
        y_tensor = torch.tensor(y, dtype=torch.long)
        train_ds = torch.utils.data.TensorDataset(X_tensor, y_tensor)
        train_loader = torch.utils.data.DataLoader(train_ds,
                                                   batch_size=self.batch_size,
                                                   shuffle=True)

        # If validation provided, move to device
        if X_val is not None and y_val is not None:
            X_val_t = torch.tensor(X_val, dtype=torch.float32).to(device)
            y_val_t = torch.tensor(y_val, dtype=torch.long).to(device)

        # Precompute quantization step
        levels = 100
        step = (self.W_max - self.W_min) / (levels - 1)

        for epoch in range(1, self.epochs + 1):
            self.model.train()
            total_loss = 0.0

            for batch_X, batch_y in train_loader:
                batch_X = batch_X.to(device)
                batch_y = batch_y.to(device)

                optimizer.zero_grad()
                outputs = self.model(batch_X)
                loss = criterion(outputs, batch_y)
                loss.backward()

                # --- Debug: print gradient norms for first layer ---
                grad_norm = self.model.fc1.weight.grad.norm().item()
                print(f"[Epoch {epoch}] Grad norm (fc1 weight): {grad_norm:.4f}")

                # Standard optimizer step
                optimizer.step()

                # --- Optional: Custom synaptic updates (post-SGD) ---
                with torch.no_grad():
                    for param in self.model.parameters():
                        if param.grad is None:
                            continue
                        # manual asymmetric update (if desired)
                        if False:  # set to True to test manual update
                            grad = param.grad
                            lr_mat = torch.where(grad >= 0,
                                                 torch.tensor(self.lr_neg, device=device),
                                                 torch.tensor(self.lr_pos, device=device))
                            param.data -= lr_mat * grad

                        # Retention drift
                        if self.retain:
                            param.data -= self.retention * (param.data - self.W_min)

                        # Clip
                        param.data.clamp_(self.W_min, self.W_max)

                        # Quantize
                        if self.quantize:
                            param.data = torch.round((param.data - self.W_min) / step) * step + self.W_min

                total_loss += loss.item()

            # Validation accuracy
            if X_val is not None and y_val is not None:
                self.model.eval()
                with torch.no_grad():
                    val_out = self.model(X_val_t)
                    _, val_pred = torch.max(val_out, dim=1)
                    val_acc = (val_pred == y_val_t).float().mean().item() * 100
                print(f"Epoch {epoch}/{self.epochs}: Loss {total_loss/len(train_loader):.4f}, "
                      f"Val Acc: {val_acc:.2f}%")

        return self

    def predict(self, X):
        if self.model is None:
            raise RuntimeError("Model not trained yet.")
        device = torch.device(self.device if self.device
                              else ('cuda' if torch.cuda.is_available() else 'cpu'))
        self.model.eval()
        X_t = torch.tensor(X, dtype=torch.float32).to(device)
        with torch.no_grad():
            out = self.model(X_t)
            _, pred = torch.max(out, dim=1)
        return pred.cpu().numpy()

# -----------------------------------
# 4) 5-fold Stratified CV
# -----------------------------------
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
fold_accs = []
fold_cms  = []

for fold, (tr_idx, te_idx) in enumerate(skf.split(X_all, y_all), 1):
    print(f"\n=== Fold {fold} ===")
    X_tr, X_te = X_all[tr_idx], X_all[te_idx]
    y_tr, y_te = y_all[tr_idx], y_all[te_idx]

    # Disable quantization & retention for initial debug run
    model = PyTorchNNWrapper(epochs=10,    # fewer epochs for quick check
                              batch_size=128,
                              quantize=False,
                              retain=False,
                              random_state=fold)
    model.fit(X_tr, y_tr, X_val=X_te, y_val=y_te)

    y_pred = model.predict(X_te)
    acc = (y_pred == y_te).mean() * 100
    cm  = confusion_matrix(y_te, y_pred)

    fold_accs.append(acc)
    fold_cms.append(cm)

    print(f"Fold {fold} final accuracy: {acc:.2f}%")
    print(f"Fold {fold} confusion matrix:\n{cm}")

# Aggregate results
mean_cm  = sum(fold_cms) / len(fold_cms)
mean_acc = np.mean(fold_accs)
std_acc  = np.std(fold_accs)
print("\nMean Confusion Matrix:\n", mean_cm)
print(f"Mean Accuracy: {mean_acc:.2f}% ± {std_acc:.2f}%")
