# Cumulative Probability Analysis

A Python/Tkinter script to compute and visualize cumulative probability distributions of conductance changes (“ΔG”) across defined conductance states for potentiation and depression pulses from an EIS CSV data file.

## Features

- **CSV Input** via file dialog (Tkinter)  
- **Data Parsing** with pandas and NumPy  
- **State Binning**:  
  - Divides conductance range into 100 equally spaced states for potentiation (pulses 1–100) and depression (pulses 101–200)  
  - Assigns each ΔG (`G per pulse (S)`) to its conductance state  
- **Statistical Analysis**:  
  - Fits a normal distribution to ΔG in each state (when ≥ 5 points) using SciPy  
  - Computes cumulative probabilities (CDF) for each ΔG  
- **Visualization**:  
  - Scatter‐plots ΔG vs. conductance state, color‐coded by CDF for potentiation and depression  
- **Data Export**:  
  - Saves tab-delimited `.txt` files with columns `Conductance`, `Delta G values`, and `Cumulative Probability` for potentiation and depression

## Prerequisites

- Python 3.x  
- pandas  
- NumPy  
- SciPy  
- Matplotlib  
- Tkinter (included in standard Python)

Install dependencies with:
```bash
pip install pandas numpy scipy matplotlib
````

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/<your-username>/cumulative-probability-analysis.git
   cd cumulative-probability-analysis
   ```
2. (Optional) Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate    # macOS/Linux
   venv\Scripts\activate       # Windows
   ```

## Usage

Run the script:

```bash
python cumulative_probability_analysis.py
```

1. Select your input CSV file when prompted.
2. View the potentiation‐pulse CDF scatter‐plot.
3. Choose an output directory when prompted.
4. Inspect or share:

   * `<basename>_CDF_potentiation.txt`
   * `<basename>_CDF_depression.txt`
5. View the depression‐pulse CDF scatter‐plot.

## Customization

* **Pulse Ranges**: Adjust the numeric ranges for potentiation/depression masks.
* **State Count**: Change `num=100` in `np.linspace` to use more or fewer conductance states.
* **Plot Style**: Modify `cmap='viridis'`, marker styles, or figure size in the plotting sections.
* **Statistical Model**: Replace `norm.fit`/`norm.cdf` with a different distribution if needed.

## Contributing

1. Fork the repo.
2. Create a branch:

   ```bash
   git checkout -b feature/YourFeature
   ```
3. Commit your changes:

   ```bash
   git commit -m "Add YourFeature"
   ```
4. Push & open a Pull Request:

   ```bash
   git push origin feature/YourFeature
   ```

