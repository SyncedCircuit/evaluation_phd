# Linearity Fit and Plot

A Python/Tkinter script to fit exponential conductance change curves for potentiation and depression phases and visualize results.

## Features

- **GUI file selection** using Tkinter: choose one or more tab-delimited `.txt` files.  
- **Data extraction**: reads pulse number, potentiation conductance, and depression conductance from each file.  
- **Parameter estimation**: fits both potentiation and depression data to a first-order exponential model  
  \[
    G(x) = \frac{G_{\max} - G_{\min}}{1 - e^{-v}} \bigl(1 - e^{-v\,\frac{x}{N}}\bigr) + G_{\min},
  \]  
  using `scipy.optimize.curve_fit`.  
- **Goodness-of-fit**: computes R² for each fit.  
- **Batch processing**: writes results for all selected files to `fitting_results.txt` with columns:  
  `File Name`, `G_max_p`, `G_min_p`, `G_max_d`, `G_min_d`, `v_p`, `R-squared_p`, `v_d`, `R-squared_d`.  
- **Visualization**: if only one file is selected, displays Matplotlib plots for potentiation and depression data with fitted curves.

## Prerequisites

- Python 3.x  
- NumPy  
- SciPy  
- Matplotlib  
- Tkinter (bundled with Python)

Install dependencies:
```bash
pip install numpy scipy matplotlib
````

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/<your-username>/linearity-fit-plot.git
   cd linearity-fit-plot
   ```
2. (Optional) Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate    # macOS/Linux
   venv\Scripts\activate       # Windows
   ```

## Usage

```bash
python linearity_fit_and_plot.py
```

1. Select one or more tab-delimited `.txt` files when prompted (header row + columns: pulse number, potentiation conductance, depression conductance).
2. The script writes `fitting_results.txt` in the same directory as your input files with fit parameters and R² values.
3. If only one file is selected, a window with two plots (potentiation and depression fits) will appear.

## Customization

* **Model functions**: edit `fitting_function_potentiation` and `fitting_function_depression` to change the fit equation.
* **Output filename**: modify `"fitting_results.txt"` in `fit_data()` to change where results are saved.
* **Plot styling**: adjust figure size, labels, or colors in the plotting block.
* **Data parsing**: tweak `delimiter` or `skiprows` in `read_data()` for different file formats.
