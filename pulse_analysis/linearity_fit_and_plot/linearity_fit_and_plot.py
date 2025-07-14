import os
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from scipy.optimize import curve_fit

# Fit parameters and assess goodness of fit
def fit_and_assess(pulse_numbers, conductance, fitting_function):
    popt, _ = curve_fit(fitting_function, pulse_numbers, conductance, method='lm')
    residuals = conductance - fitting_function(pulse_numbers, *popt)
    ss_res = np.sum(residuals ** 2)
    ss_tot = np.sum((conductance - np.mean(conductance)) ** 2)
    r_squared = 1 - (ss_res / ss_tot)
    return popt, r_squared

# Read data from file
def read_data(file_path):
    with open(file_path, 'r') as file:
        next(file)  # Skip header
        data = np.loadtxt(file, delimiter='\t', skiprows=1)
    pulse_numbers = data[:, 0]
    potentiation_conductance = data[:, 1]
    depression_conductance = data[:, 2]
    max_pulse_number = int(pulse_numbers[-1])  # Determine maximum pulse number

    # Calculate G_max_p, G_min_p, G_max_d, G_min_d
    G_max_p = np.max(potentiation_conductance)
    G_min_p = np.min(potentiation_conductance)
    G_max_d = np.max(depression_conductance)
    G_min_d = np.min(depression_conductance)

    # Print calculated values
    print("Calculated Values:")
    print(f"G_max_p: {G_max_p}")
    print(f"G_min_p: {G_min_p}")
    print(f"G_max_d: {G_max_d}")
    print(f"G_min_d: {G_min_d}")

    return pulse_numbers, potentiation_conductance, depression_conductance, max_pulse_number, G_max_p, G_min_p, G_max_d, G_min_d


# Main fitting function
def fit_data():
    # Open file dialog to select input files
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_paths = filedialog.askopenfilenames(title="Select Text Files", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    root.destroy()  # Close the Tkinter window after file selection

    if not file_paths:
        print("No files selected. Exiting...")
        return

    # Write headers to the export file
    output_file_path = os.path.join(os.path.dirname(file_paths[0]), "fitting_results.txt")
    with open(output_file_path, 'w') as output_file:
        output_file.write("File Name\tG_max_p\tG_min_p\tG_max_d\tG_min_d\tv_p\tR-squared_p\tv_d\tR-squared_d\n")

    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        print(f"Fitting data from {file_name}")

        # Read data from file
        pulse_numbers, potentiation_conductance, depression_conductance, max_pulse_number, G_max_p, G_min_p, G_max_d, G_min_d = read_data(file_path)

        # Define fitting functions
        def fitting_function_potentiation(x, v):
            return ((G_max_p - G_min_p) / (1 - np.exp(-v))) * (1 - np.exp(-v * (x / max_pulse_number))) + G_min_p

        def fitting_function_depression(x, v):
            return ((G_max_p - G_min_p) / (1 - np.exp(-v))) * (1 - np.exp(-v * (x / max_pulse_number))) + G_min_p
            #G_max_d - ((G_max_d - G_min_d) / (1 - np.exp(-v))) * (1 - np.exp(-v)) * (1 - np.exp(-v * (1 - (x / max_pulse_number))))

        # Fit potentiation parameters
        popt_p, r_squared_p = fit_and_assess(pulse_numbers, potentiation_conductance, fitting_function_potentiation)

        # Fit depression parameters
        popt_d, r_squared_d = fit_and_assess(pulse_numbers, depression_conductance, fitting_function_depression)

        # Append fitting results to the export file
        with open(output_file_path, 'a') as output_file:
            output_file.write(f"{file_name}\t{G_max_p}\t{G_min_p}\t{G_max_d}\t{G_min_d}\t{popt_p[0]}\t{r_squared_p}\t{popt_d[0]}\t{r_squared_d}\n")

        # Plot data and fitting if only one file is selected
        if len(file_paths) == 1:
            plt.figure(figsize=(10, 6))

            # Plot potentiation data and fitting
            plt.subplot(2, 1, 1)
            plt.scatter(pulse_numbers, potentiation_conductance, label='Potentiation Data', color='blue')
            plt.plot(pulse_numbers, fitting_function_potentiation(pulse_numbers, *popt_p), label='Fitted Curve', color='red')
            plt.title('Potentiation')
            plt.xlabel('Pulse Number')
            plt.ylabel('Conductance')
            plt.legend()

            # Plot depression data and fitting
            plt.subplot(2, 1, 2)
            plt.scatter(pulse_numbers, depression_conductance, label='Depression Data', color='green')
            plt.plot(pulse_numbers, fitting_function_depression(pulse_numbers, *popt_d), label='Fitted Curve', color='orange')
            plt.title('Depression')
            plt.xlabel('Pulse Number')
            plt.ylabel('Conductance')
            plt.legend()

            plt.tight_layout()
            plt.show()

    print("Fitting results saved.")

if __name__ == "__main__":
    fit_data()
