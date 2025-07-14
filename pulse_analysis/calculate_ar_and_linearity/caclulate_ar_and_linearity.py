import tkinter as tk
from tkinter import filedialog
import numpy as np
from scipy.optimize import curve_fit

def calculate_AR(pulses_data):
    # Extract data from the pulses_data
    conductivity = pulses_data[:, 1]
    delta_conductivity = pulses_data[:, 2]
    conductance = pulses_data[:, 3]
    delta_conductance = pulses_data[:, 4]

    # Split data into potentiation and depression phases
    num_pulses = len(conductivity) // 2
    Gp = conductance[:num_pulses+1]
    Gd = conductance[num_pulses:]

    # Find the maximum pulse number
    max_pulse_number = len(Gp)

    # Calculate the maximum absolute difference between Gp and Gd
    max_diff = np.max(np.abs(Gp - np.flip(Gd)))

    # Calculate the total change in conductance
    total_change = conductance[-1] - conductance[num_pulses - 1]

    # Calculate the asymmetric ratio (AR)
    AR = abs(max_diff / total_change)

    return AR

def calculate_linearity(conductance, num_pulses):
    def linear_func(pulse_number, alpha):
        return ((conductance[-1]**alpha - conductance[num_pulses - 1]**alpha) * pulse_number + conductance[num_pulses - 1]**alpha)**(1/alpha)

    pulse_numbers = np.arange(1, num_pulses + 1)
    try:
        popt, _ = curve_fit(linear_func, pulse_numbers, conductance)
        alpha = popt[0]
    except:
        alpha = None

    return alpha

def calculate_AR_and_linearity_from_file(file_path):
    try:
        pulses_data = np.loadtxt(file_path, skiprows=1, delimiter='\t')
        conductivity = pulses_data[:, 1]
        conductance = pulses_data[:, 3]
        num_pulses = len(conductivity) // 2
        AR = calculate_AR(pulses_data)
        alpha_potentiation = calculate_linearity(conductance[:num_pulses+1], num_pulses)
        alpha_depression = calculate_linearity(conductance[num_pulses:], num_pulses)
        return AR, alpha_potentiation, alpha_depression
    except Exception as e:
        return None, None, None

def select_files():
    file_paths = filedialog.askopenfilenames(initialdir=r'C:\Users\plangner\OneDrive - IREC-edu\00 - PhD\00 - Samples', title="Select Files")
    for file_path in file_paths:
        AR, alpha_potentiation, alpha_depression = calculate_AR_and_linearity_from_file(file_path)
        if AR is not None:
            print(f"File: {file_path}, AR: {AR}, Alpha (Potentiation): {alpha_potentiation}, Alpha (Depression): {alpha_depression}")
        else:
            print(f"Error processing file: {file_path}")

# Create GUI window
root = tk.Tk()
root.title("Asymmetric Ratio and Linearity Overview")

# Create button to select files
select_files_button = tk.Button(root, text="Select Files", command=select_files)
select_files_button.pack(pady=10)

# Run the GUI
root.mainloop()
