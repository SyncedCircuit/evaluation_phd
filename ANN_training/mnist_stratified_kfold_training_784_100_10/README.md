# MNIST Stratified K-Fold Training

A PyTorch script that trains a simple MLP on the MNIST dataset using 5-fold stratified cross-validation, with optional weight quantization and retention drift.

## Features

- **Data loading & preprocessing**  
  - Downloads MNIST, flattens 28×28 images to 784-dim vectors, normalizes to [0,1].  
  - Combines train and test sets for cross-validation.

- **Model architecture**  
  - Two-layer MLP: 784 → 100 (ReLU) → 10 output logits.  

- **sklearn-compatible wrapper**  
  - `PyTorchNNWrapper` implements `fit`/`predict`, so you can swap in any scikit-learn CV loop.  
  - Supports:
  - Asymmetric learning rates (`lr_pos`, `lr_neg`)  
  - Retention drift toward `W_min`  
  - Weight clipping to `[W_min, W_max]`  
  - Discrete quantization to fixed levels  
  - Custom epochs, batch size, device, and random seed  

- **Training & evaluation**  
  - 5-fold `StratifiedKFold` (shuffle, `random_state=42`)  
  - Prints gradient norms each batch for the first layer  
  - Reports per-fold loss, validation accuracy, confusion matrix, and final accuracy  
  - Aggregates mean confusion matrix and mean ± std accuracy across folds  

## Prerequisites

- Python 3.x  
- PyTorch  
- torchvision  
- numpy  
- scikit-learn  

Install with:
```bash
pip install torch torchvision numpy scikit-learn
````

## Usage

```bash
python mnist_stratified_kfold_training_784_100_10.py
```

This will:

1. Load and preprocess MNIST.
2. Run 5-fold CV (10 epochs per fold, batch size 128 by default).
3. Print gradient norms, epoch losses, validation accuracy.
4. Display per-fold accuracy & confusion matrices.
5. Print mean accuracy ± std and the averaged confusion matrix.

## Customization

* **Hyperparameters**: edit `PyTorchNNWrapper` initialization for `epochs`, `batch_size`, `lr_pos`, `lr_neg`, `retention`, `W_min`, `W_max`, `quantize`, `retain`, `device`, `random_state`.
* **CV settings**: change `n_splits`, `shuffle`, or seed in `StratifiedKFold`.
* **Asymmetric updates**: enable manual updates by toggling the flag in the `fit` loop.
