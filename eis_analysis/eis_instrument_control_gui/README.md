# CLI PPF Curve Fitting Tool

**File:** `eis_instrumen_control_gui.py`

A simple command-line utility that fits paired-pulse facilitation (PPF) data to a double-exponential model. Users enter time (Δt) and plasticity (%) values interactively, and the script returns best-fit parameters and their uncertainties.

## Features

- **PPF Model:**  
  \(y(Δt) = C1\,e^{-Δt/τ1} + C2\,e^{-Δt/τ2}\)
- **Interactive Input:**  
  Prompts for four Δt (seconds) and four plasticity (%) values.
- **Non-linear Fit:**  
  Uses `scipy.optimize.curve_fit` with user-defined initial guesses.
- **Output:**  
  Prints fitted values of C1, C2, τ1, τ2 with standard errors.

## Requirements

- Python 3.x  
- NumPy  
- SciPy  

```bash
pip install numpy scipy

