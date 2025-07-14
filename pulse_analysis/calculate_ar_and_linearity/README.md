# Asymmetric Ratio and Linearity Overview

A Python/Tkinter script to compute asymmetric ratio (AR) and linearity (α) metrics for potentiation and depression pulses from tab-delimited data files.

## Features

- **GUI file selection**: Select one or more `.txt` files via a Tkinter dialog.  
- **Asymmetric Ratio (AR)**:  
  - Splits conductance data into potentiation and depression halves  
  - Computes maximum absolute difference and total conductance change  
  - Calculates AR = |max_diff / total_change|  
- **Linearity (α)**:  
  - Fits a power-law model to conductance vs. pulse number using `scipy.optimize.curve_fit`  
  - Reports α for potentiation and depression phases  
- **Batch processing**: Prints `File: <path>, AR: <value>, Alpha (Potentiation): <value>, Alpha (Depression): <value>` for each file.

## Prerequisites

- Python 3.x  
- `numpy`  
- `scipy`  
- `tkinter` (usually included with Python)

Install dependencies:
```bash
pip install numpy scipy
````

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/<your-username>/asymmetric-ratio-linearity.git
   cd asymmetric-ratio-linearity
   ```

2. (Optional) Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows
   ```

## Usage

```bash
python caclulate_ar_and_linearity.py
```

1. Click **Select Files** in the GUI window.
2. Choose one or more tab-delimited `.txt` files (first row header, columns: any, conductivity, Δconductivity, conductance, Δconductance).
3. View the console output:

   ```
   File: path/to/data.txt, AR: 0.1234, Alpha (Potentiation): 1.05, Alpha (Depression): 0.98
   ```

## Customization

* **Default folder**: Change `initialdir` in `select_files()` for a different starting directory.
* **File parsing**: Modify `delimiter` or `skiprows` in `np.loadtxt` to match your file format.
* **Column indices**: Update indices in `calculate_AR()` if your data columns differ.
* **Model function**: Edit `linear_func` in `calculate_linearity()` to test other fitting models.
