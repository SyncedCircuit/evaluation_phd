# EIS Instrument Control GUI

A simple Python CLI application to fit paired-pulse facilitation (PPF) curves to experimental data using NumPy and SciPy. Prompts for time intervals (Δt) and plasticity (%) values, performs nonlinear curve fitting, and outputs best-fit parameters with uncertainties.

## Features

* Prompt for **x-values** (time Δt in seconds) and **y-values** (plasticity in %)
* Fit PPF equation:
  σ(Δt) = C1·exp(−Δt/τ1) + C2·exp(−Δt/τ2)
* Compute best-fit parameters:

  * **C1**, **C2** (amplitude coefficients)
  * **τ1**, **τ2** (time constants)
* Report parameter uncertainties from covariance matrix
* Lightweight, command-line only (no GUI dependencies)

## Prerequisites

* Python 3.x
* NumPy
* SciPy

Install dependencies with:

```
pip install numpy scipy
```

## Installation

1. Clone this repository:

   ```
   git clone https://github.com/<your-username>/eis-instrument-control.git
   cd eis-instrument-control
   ```
2. (Optional) Create and activate a virtual environment:

   ```
   python3 -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows
   ```
3. Install required packages:

   ```
   pip install numpy scipy
   ```

## Usage

Run the script and follow prompts:

```
python eis_instrumen_control_gui.py
```

1. When prompted, enter **x-values** (space-separated Δt in seconds).
2. Enter **y-values** (space-separated plasticity in %).
3. View fitted parameters and their uncertainties.

Example:

```
Gib die x-Werte (Zeit in Sekunden) ein:
0.1 0.5 1.0 2.0
Gib die y-Werte (Plasticity in %) ein:
120 95 60 30
Fit-Ergebnisse:
C1 = 85.2 +/- 4.1
C2 = 40.3 +/- 2.8
tau1 = 0.75 +/- 0.05
tau2 = 1.8 +/- 0.1
```

## Customization

* Modify the `ppf_equation` function to change the model form.
* Adjust `initial_guess` in the script for different starting parameters.

## Contributing

1. Fork the repository.
2. Create a branch:

   ```
   git checkout -b feature/YourFeature
   ```
3. Commit your changes:

   ```
   git commit -m "Add YourFeature"
   ```
4. Push and open a Pull Request:

   ```
   git push origin feature/YourFeature
   ```

