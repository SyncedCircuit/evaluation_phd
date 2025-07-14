# Conductivity Calculator

A simple Python/Tkinter GUI application to calculate electrical conductivity (σ) and conductance (G) of a rectangular sample based on its dimensions and resistance. Supports input in micrometers or nanometers and outputs conductivity in S/cm and conductance in siemens (S).

## Features

* Input sample length (L), width (w), thickness (t) and resistance (R)
* Unit conversion between micrometers and nanometers
* Instant calculation of:

  * **Conductivity (σ)** in S/cm:
    σ = (L / (w × t)) / R
  * **Conductance (G)** in S:
    G = 1 / R
* Lightweight GUI built with Tkinter
* Easily customizable image, layout and formula display

## Prerequisites

* Python 3.x
* Tkinter (usually included in standard Python installations)

## Installation

1. Clone this repository:

   ```
   git clone https://github.com/<your-username>/conductivity-calculator.git
   cd conductivity-calculator
   ```
2. (Optional) Create and activate a virtual environment:

   ```
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```
3. Run the application:

   ```
   python calculator_conductivity.py
   ```

## Usage

1. Enter the **Length**, **Width**, and **Thickness** of your sample.
2. Select the unit (`micrometer` or `nanometer`).
3. Enter the **Resistance (Ω)**.
4. Click **Calculate**.
5. Read the displayed conductivity and conductance values.

> **Note:** Update the `image_file` path in `calculator_conductivity.py` to point to your local geometry illustration (or remove the image block if not needed).

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m "Add YourFeature"`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a Pull Request.
