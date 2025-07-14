# Impedance Spectroscopy UI

This module defines the graphical user interface for the Impedance Spectroscopy tool, generated via Qt Designer and PyQt4.

## Features

- **Equipment Connection**  
  Detect and connect to instruments (real or pyVISA-sim)  
- **Calibration (Compensation)**  
  Perform short/open calibration or skip  
- **Analysis Parameters**  
  • Frequency sweep (start/stop, linear/log, points)  
  • Voltage & bandwidth settings  
  • Optional point averaging  
- **Sample Definition**  
  • Enter sample ID, data folder, diameter & thickness (mm)  
  • Free-form notes field  
- **Plot Controls**  
  Switch among permittivity (ε′/ε″), complex impedance (Z/Θ), R/C, Zr vs Zi, or custom graphs  
- **Programmed Analysis**  
  Batch-run or delete saved analyses  

## Requirements

- Python 3.x  
- PyQt4  
- pyVISA (for instrument communication)  
- matplotlib & numpy (for backend plotting & data processing)

Install dependencies:
```bash
pip install pyqt4 pyvisa matplotlib numpy

