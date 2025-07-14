# MNIST Parameter Variation Training (64-54-10)

A PyTorch script that trains a simple multi-layer perceptron on the sklearn digits dataset (64 inputs) using 5-fold stratified cross-validation, comparing a custom synaptic weight update rule to a baseline SGD update.

## Features

- **Data loading & preprocessing**  
  - Loads digits dataset from `sklearn.datasets`  
  - Standardizes features with `StandardScaler`
- **Model architecture**  
  - Three-layer MLP:  
    - Input: 64 features  
    - Hidden layers: 54 × `num_states` units with Tanh activation  
    - Output: 10 classes
- **Custom synaptic weight update**  
  - Asymmetric update using `asymmetric_ratio`, `retention_rate`, `dynamic_range`, `G_max`, `G_min`, and voltage parameter `v`  
  - Applied in `PyTorchClassifier` when `use_custom_update=True`
- **Training & evaluation**  
  - 5-fold `StratifiedKFold` cross-validation (`random_state=42`)  
  - Prints per-epoch loss and test accuracy for each fold  
  - Compares mean accuracy ± std between custom and baseline models

## Prerequisites

- Python 3.x  
- PyTorch  
- numpy  
- scikit-learn  

Install dependencies:
```bash
pip install torch numpy scikit-learn
````

## Usage

Run the script:

```bash
python mnist_parameter_variation_training_64_54_10.py
```

This will:

1. Load and preprocess the digits dataset.
2. Perform 5-fold stratified cross-validation.
3. For each fold, train both the custom-update model and the baseline model.
4. Print per-epoch loss and test accuracy.
5. Display final mean accuracies ± standard deviation.

## Customization

* **Synaptic update parameters**: edit `num_states`, `asymmetric_ratio`, `retention_rate`, `dynamic_range`, `G_max`, `G_min`, and `v` at the top of the script.
* **Training settings**: change `num_epochs`, batch size (default 64), learning rate (default 0.001), and momentum in the `SGD` optimizer.
* **Toggle update rule**: set `use_custom_update` in `PyTorchClassifier` to enable/disable the custom update.
* **Cross-validation**: adjust `n_splits`, `shuffle`, or `random_state` in `StratifiedKFold`.
