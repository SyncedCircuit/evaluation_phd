# Agilent to ZView EIS Nyquist Plot

A Python script to convert Agilent EIS CSV files into ZView-compatible `.txt` files and generate Nyquist plots (individual and combined).

## Features

- GUI file selection for multiple input files (Tkinter `askopenfilenames`)  
- GUI directory selection for output (Tkinter `askdirectory`)  
- Converts each Agilent CSV (whitespace-delimited, header skipped) to tab-delimited `.txt` (Frequency, Real, Imaginary)  
- Generates individual Nyquist plots (`<basename>_nyquist.png`) for each dataset  
- Compiles a combined Nyquist plot for all selected files (`nyquist_all.png`) with color-coded traces  
- Easily extendable to include Bode plots (commented out)

## Prerequisites

- Python 3.x  
- NumPy  
- pandas  
- Matplotlib  
- Tkinter (included in standard Python)

Install dependencies:
```bash
pip install numpy pandas matplotlib
````

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/<your-username>/agilent-to-zview-eis.git
   cd agilent-to-zview-eis
   ```
2. (Optional) Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

## Usage

Run the script:

```bash
python agilent_to_zview_eis_nyquist_plot.py
```

1. Select one or more Agilent EIS CSV files when prompted.
2. Choose an output directory for the generated files.
3. For each input file you’ll get:

   * `<basename>.txt`: tab-delimited data (Frequency, Real, Imaginary)
   * `<basename>_nyquist.png`: Nyquist plot image
4. A combined plot `nyquist_all.png` will be saved in the output directory.

## Customization

* **Delimiter/Header**: Modify the `np.genfromtxt` call for different formats.
* **Plots**: Un-comment and customize the Bode plot section.
* **Color Map**: Change `cmap = plt.get_cmap('coolwarm')` to another Matplotlib colormap.

