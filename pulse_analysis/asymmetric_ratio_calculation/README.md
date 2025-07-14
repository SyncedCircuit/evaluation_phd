# Asymmetric Ratio Calculation

A Python/Tkinter script to split pulse data into two halves and compute asymmetric ratios between potentiation and depression pulses.

## Features

- **List splitting utility**  
  - Reads a tab-delimited `.txt` file, splits its data into two halves (appending the first value of the second half to the end of the first), and saves each with the original header.  
- **GUI file selection**  
  - Prompts the user to choose potentiation and depression pulse files via a Tkinter dialog.  
- **Asymmetric ratio calculation**  
  - Computes maximum absolute differences across four metrics (e.g., conductivity, Δconductivity, conductance, Δconductance)  
  - Calculates asymmetric ratios based on the last pulse values in each dataset  
- **Configurable paths**  
  - Default input/output file paths and initial directory can be customized in the script.

## Prerequisites

- Python 3.x  
- Tkinter (bundled with standard Python distributions)

## Installation

```bash
git clone https://github.com/<your-username>/asymmetric-ratio-calculation.git
cd asymmetric-ratio-calculation
````

## Usage

```bash
python asymmetric_ratio_calculation.py
```

1. **Static splitting**

   * The script will first split the hard-coded input file into two output files (`*_first_half_with_header.txt` and `*_second_half_with_header.txt`).
2. **Interactive ratio tool**

   * A window appears prompting you to select your potentiation pulses file.
   * After selection, choose your depression pulses file.
   * The script prints the maximum differences and the computed asymmetric ratios to the console, then closes the GUI.

## Customization

* **Input/Output paths**: Edit the `file_path`, `first_half_path`, and `second_half_path` variables at the top of the script.
* **Initial directory**: Change the `initialdir` argument in `browse_file()` to point to your default folder.
* **Metric count**: Adjust the length of `max_differences` and the indexing in `calculate_asymmetric_ratio()` if your data has more or fewer columns.

