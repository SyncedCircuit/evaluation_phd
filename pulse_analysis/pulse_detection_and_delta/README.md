# Pulse Detection & Delta Analysis

**File:** `pulse_detection_and_delta.py`

A GUI tool to batch‐process CSV files of resistance and pulse amplitude data, compute conductivity and conductance, detect individual pulses by thresholding, calculate per-pulse averages and deltas relative to the first pulse, and export results and summary graphs.

## Features

- **Batch Processing:** Select multiple CSV files at once.  
- **Conductivity & Conductance:**  
  - Converts resistance (`CHRES` column) to conductivity (S/cm) and conductance (S) using user-entered sample geometry.  
- **Pulse Detection:**  
  - Threshold on a specified data column to identify pulse events.  
- **Delta Analysis:**  
  - Computes average conductivity/conductance per pulse and Δ relative to the first pulse.  
- **Outputs:**  
  - Per‐file raw data (`*_raw_data.txt`) with added columns.  
  - Per‐file pulse list (`*_pulse_list.txt`) with pulse number, value, and delta.  
  - Combined conductivity and conductance graphs (`conductivity_graph.png`, `conductance_graph.png`).

## Requirements

- Python 3.x  
- `matplotlib`  
- `Pillow`  
- `tkinter` (bundled with most Python installs)

```bash
pip install matplotlib Pillow
````

## Usage

```bash
python pulse_detection_and_delta.py
```

1. **Pulses Column Header:** Enter the exact CSV header for pulse amplitudes.
2. **Sample Geometry:** Enter Length (L), Width (W), Thickness (th) in µm.
3. **Select CSV Files:** Choose one or more input CSVs.
4. **Select Output Directory:** Choose where TXT files and graphs will be saved.
5. **Threshold Value:** Enter pulse amplitude threshold (same units as your column).

The tool will generate:

* `<name>_raw_data.txt`
* `<name>_pulse_list.txt`
* `conductivity_graph.png`
* `conductance_graph.png`

## Input Format

* CSV with header row including:

  * `CHRES` (resistance)
  * The user-specified pulse amplitude column

## Output Files

* **`*_raw_data.txt`** (TSV): original data + `Conductivity (S/cm)` and `Conductance (S)`
* **`*_pulse_list.txt`** (TSV):

  ```
  Pulse Number | Conductivity (S/cm) | Delta Conductivity (S/cm) | Conductance (S) | Delta Conductance (S)
  ```
* **Graphs:**

  * `conductivity_graph.png`
  * `conductance_graph.png`

## Notes

* Images: if `Geometry EGT_2.png` exists in the working directory, it will be displayed in the GUI.
* Geometry inputs assume µm units; conversions to cm are handled internally.
* Adjust the threshold and sample geometry to match your experimental setup.
