# Impedance Spectroscopy UI

A PyQt4 GUI for controlling impedance spectroscopy measurements, including equipment connection, calibration, real-time analysis, and batch programming. Auto-generated UI code from Qt Designer.

## Features

* **Equipment Connection**

  * Detect instruments via pyVISA or pyVISA-sim
  * Connect/disconnect and display instrument ID
* **Compensation Calibration**

  * Short, Open or Skip routines
* **Real-Time Analysis**

  * Frequency sweep: start/stop frequencies, number of points, logarithmic or linear scale
  * Voltage, bandwidth and optional point averaging
  * Plot ε′ & ε″ vs. ƒ, Z & Θ vs. ƒ, R & C vs. ƒ, Z′ vs. Z″
* **Sample Management**

  * Enter sample ID, save folder, diameter, thickness and notes
* **Programmed Batch Analysis**

  * Queue multiple samples
  * View and delete selected runs
  * Start automated sequence

## Prerequisites

* **Python 3.x**
* **PyQt4**
* **pyVISA**
* **NumPy**
* **SciPy**
* **Matplotlib** or **pyqtgraph** (for plotting)
* *(Optional)* **pyVISA-sim** for hardware-free testing

Install dependencies:

```bash
pip install PyQt4 pyvisa numpy scipy matplotlib pyqtgraph
```

## Installation

1. **Clone** the repository:

   ```bash
   git clone https://github.com/<your-username>/impedance-spectroscopy-gui.git
   cd impedance-spectroscopy-gui
   ```
2. *(Optional)* **Create & activate** a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows
   ```
3. **Install** prerequisites as above.

## Usage

1. **Connect** your impedance analyzer and ensure it’s visible to pyVISA.
2. **Launch** the app (replace `main.py` with your entry-point script):

   ```bash
   python main.py
   ```
3. **Navigate** tabs:

   * **Connection & Compensation**: Detect, connect, calibrate.
   * **Analysis**: Configure sweep, enter sample data, run measurement, view plots.
   * **Program Analysis**: Queue and manage batch runs; delete or start programmed analysis.

### Quick UI Test

To preview the UI without backend logic, run:

```python
from PyQt4 import QtGui
from impedance_spectroscopy_ui import Ui_MainWindow

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
```

## Customization

* **Layout**: Edit the original `.ui` file in Qt Designer and regenerate with `pyuic4`.
* **Functionality**: Connect widgets to your instrument-control and data-processing code in your main script.
* **Styling**: Adjust fonts, sizes or add custom icons via Qt Designer or stylesheet.

## Contributing

1. **Fork** the repo.
2. **Branch**: `git checkout -b feature/YourFeature`
3. **Commit**: `git commit -m "Add YourFeature"`
4. **Push** & open a **Pull Request**: `git push origin feature/YourFeature`

