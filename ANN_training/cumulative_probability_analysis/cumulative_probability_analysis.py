import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import os
from tkinter import Tk, filedialog, messagebox

# Ask the user to select input CSV file
root = Tk()
root.withdraw()
file_path = filedialog.askopenfilename(initialdir='C:/Users/plangner/OneDrive - IREC-edu/00 - PhD/00 - Samples',
                                       title='Select CSV File', filetypes=[("CSV files", "*.csv")])
root.destroy()

if not file_path:
    messagebox.showinfo("Error", "No file selected. Program terminated.")
    exit()

# Load the CSV file into a pandas DataFrame
df = pd.read_csv(file_path)

# Convert 'G per pulse (S)' column to numeric values
df['G per pulse (S)'] = pd.to_numeric(df['G per pulse (S)'], errors='coerce')

# Separate potentiation and depression pulses using numpy
pulse_numbers = df['Pulse Number'].values
potentiation_mask = (pulse_numbers >= 1) & (pulse_numbers <= 100)
depression_mask = (pulse_numbers >= 101) & (pulse_numbers <= 200)

potentiation_data = df[potentiation_mask]
depression_data = df[depression_mask]

# Determine the minimum and maximum conductance values for potentiation and depression pulses
potentiation_min_conductance = potentiation_data['Conductance (S)'].min()
potentiation_max_conductance = potentiation_data['Conductance (S)'].max()

depression_min_conductance = depression_data['Conductance (S)'].min()
depression_max_conductance = depression_data['Conductance (S)'].max()

# Divide the conductance range into 100 equally sized states
potentiation_states = np.linspace(potentiation_min_conductance, potentiation_max_conductance, num=100)
depression_states = np.linspace(depression_min_conductance, depression_max_conductance, num=100)

# Assign each delta G value to its corresponding conductance state for potentiation pulses
potentiation_data['Conductance State'] = pd.cut(potentiation_data['Conductance (S)'], bins=potentiation_states, labels=False)

# Assign each delta G value to its corresponding conductance state for depression pulses
depression_data['Conductance State'] = pd.cut(depression_data['Conductance (S)'], bins=depression_states, labels=False)

# Plot delta G values vs. conductance state with color-coded cumulative probability
plt.figure(figsize=(12, 6))

# Plot for potentiation pulses
for state in potentiation_data['Conductance State'].unique():
    state_data = potentiation_data[potentiation_data['Conductance State'] == state]['G per pulse (S)']
    if len(state_data) > 5 and np.isfinite(state_data).all():
        mu, std = norm.fit(state_data)
        state_cumulative_prob = norm.cdf(state_data, mu, std)
        plt.scatter([state] * len(state_data), state_data, c=state_cumulative_prob, cmap='viridis', alpha=0.5)

# Add colorbar
cbar = plt.colorbar()
cbar.set_label('Cumulative Probability')

plt.title('Potentiation Pulses: Delta G vs. Conductance State (States with >5 values)')
plt.xlabel('Conductance State')
plt.ylabel('Delta G values')
plt.grid(True)
plt.show()

# Get the directory and filename of the original CSV file
csv_directory, csv_filename = os.path.split(file_path)
csv_filename_without_extension, csv_extension = os.path.splitext(csv_filename)

# Create a new directory for saving exported files
output_directory = filedialog.askdirectory(initialdir=csv_directory, title='Select Output Directory')
if not output_directory:
    messagebox.showinfo("Error", "No directory selected. Program terminated.")
    exit()

# Save the potentiation data to a tab-separated text file in the output directory
potentiation_export_data = pd.DataFrame(columns=['Conductance', 'Delta G values', 'Cumulative Probability'])
for state in potentiation_data['Conductance State'].unique():
    state_data = potentiation_data[potentiation_data['Conductance State'] == state]
    if len(state_data) > 5 and np.isfinite(state_data['G per pulse (S)']).all():
        mu, std = norm.fit(state_data['G per pulse (S)'])
        state_cumulative_prob = norm.cdf(state_data['G per pulse (S)'], mu, std)
        export_df = pd.DataFrame({'Conductance': state_data['Conductance (S)'],
                                  'Delta G values': state_data['G per pulse (S)'],
                                  'Cumulative Probability': state_cumulative_prob})
        potentiation_export_data = pd.concat([potentiation_export_data, export_df])

# Save the potentiation data to a tab-separated text file in the output directory
output_filename = os.path.join(output_directory, f'{csv_filename_without_extension}_CDF_potentiation.txt')
potentiation_export_data.to_csv(output_filename, sep='\t', index=False)
print(f"Potentiation data exported to {output_filename}")

# Plot for depression pulses
plt.figure(figsize=(12, 6))
for state in depression_data['Conductance State'].unique():
    state_data = depression_data[depression_data['Conductance State'] == state]['G per pulse (S)']
    if len(state_data) > 5 and np.isfinite(state_data).all():
        mu, std = norm.fit(state_data)
        state_cumulative_prob = norm.cdf(state_data, mu, std)
        plt.scatter([state] * len(state_data), state_data, c=state_cumulative_prob, cmap='viridis', alpha=0.5)

# Add colorbar
cbar = plt.colorbar()
cbar.set_label('Cumulative Probability')

plt.title('Depression Pulses: Delta G vs. Conductance State (States with >5 values)')
plt.xlabel('Conductance State')
plt.ylabel('Delta G values')
plt.grid(True)
plt.show()

# Save the depression data to a tab-separated text file in the output directory
depression_export_data = pd.DataFrame(columns=['Conductance', 'Delta G values', 'Cumulative Probability'])
for state in depression_data['Conductance State'].unique():
    state_data = depression_data[depression_data['Conductance State'] == state]
    if len(state_data) > 5 and np.isfinite(state_data['G per pulse (S)']).all():
        mu, std = norm.fit(state_data['G per pulse (S)'])
        state_cumulative_prob = norm.cdf(state_data['G per pulse (S)'], mu, std)
        export_df = pd.DataFrame({'Conductance': state_data['Conductance (S)'],
                                  'Delta G values': state_data['G per pulse (S)'],
                                  'Cumulative Probability': state_cumulative_prob})
        depression_export_data = pd.concat([depression_export_data, export_df])

# Save the depression data to a tab-separated text file in the output directory
output_filename = os.path.join(output_directory, f'{csv_filename_without_extension}_CDF_depression.txt')
depression_export_data.to_csv(output_filename, sep='\t', index=False)
print(f"Depression data exported to {output_filename}")
