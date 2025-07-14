# Weight Update Batch Processor

A Python/Tkinter script to batch-process tab-delimited `.txt` data files by computing per-pulse changes in conductivity and conductance.

## Features

- **GUI file selection**: Choose one or more `.txt` files via a file dialog.  
- **Header parsing & extension**: Reads the first line as tabs-delimited header and appends two new columns:
  - `Cond PP (S/cm)` — change in conductivity per pulse  
  - `G per pulse (S)` — change in conductance per pulse  
- **Delta computation**:  
  - Calculates Δ conductivity = current conductivity (column 2) minus previous  
  - Calculates Δ conductance = current conductance (column 4) minus previous  
- **Batch output**: Writes `<original_name>_processed.txt` for each input file, preserving all original columns plus the two new ones.

## Prerequisites

- Python 3.x  
- Tkinter (bundled with most Python installations)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/<your-username>/weight-update-batch.git
   cd weight-update-batch
   ```

2. (Optional) Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate    # macOS/Linux
   venv\Scripts\activate       # Windows
   ```

## Usage

```bash
python weight_update_batch.py
```

1. When prompted, select one or more `.txt` files containing tab-delimited data.
2. The script will process each file and print the output path, e.g.:

   ```
   Processed data written to sample_processed.txt
   ```
3. Check the output directory for the `_processed.txt` files.

## Customization

* **Starting folder**: Change the `initial_dir` path in `select_files()` to set a different default directory.
* **Column indices**: By default, conductivity is read from column index 1 and conductance from index 3—update those indices in `process_data()` if your file format differs.

