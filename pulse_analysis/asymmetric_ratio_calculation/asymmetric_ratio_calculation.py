import tkinter as tk
from tkinter import filedialog
from typing import List

# Function to split a list into two halves
def split_list(original_list: List[int]) -> tuple[List[int], List[int]]:
    # Calculate the split index
    split_index = len(original_list) // 2

    # Split the list into two sublists
    first_half = original_list[:split_index]
    second_half = original_list[split_index:]

    # Add the first value from second_half to the end of first_half
    first_half.append(second_half[0])

    return first_half, second_half

# Read data from the .txt file
file_path = r'C:\Users\plangner\OneDrive - IREC-edu\00 - PhD\00 - Samples\230627_LSAT-BCV-LSF50\Juno\230810\Result\4_300C_Ig -200nA_tp 0.6s_tsp 1.5s_50 pulses_pulse_list_processed.txt'

with open(file_path, 'r') as file:
    # Read lines from the file, keeping the header
    lines = file.readlines()

# Extract the header and remove it from the lines
header = lines[0]
lines = lines[1:]

# Convert lines to a list of lists, splitting values based on tabs
original_list = [list(map(float, line.strip().split('\t')[1:])) for line in lines]

# Add numbering starting from 0 in the "Pulse Number" column
for i, line in enumerate(original_list):
    line.insert(0, i)

# Call the function to split the list
first_half, second_half = split_list(original_list)

# Remove the first column from the second_half
second_half = [line[1:] for line in second_half]

# Add numbering starting from 0 in the "Pulse Number" column for the second_half
for i, line in enumerate(second_half):
    line.insert(0, i)

# Specify the output file paths
first_half_path = r'C:\Users\plangner\OneDrive - IREC-edu\00 - PhD\00 - Samples\230627_LSAT-BCV-LSF50\Juno\230810\Result\4_300C_Ig -200nA_tp 0.6s_tsp 1.5s_50 pulses_pulse_list_processed_first_half_with_header.txt'
second_half_path = r'C:\Users\plangner\OneDrive - IREC-edu\00 - PhD\00 - Samples\230627_LSAT-BCV-LSF50\Juno\230810\Result\4_300C_Ig -200nA_tp 0.6s_tsp 1.5s_50 pulses_pulse_list_processed_second_half_with_header.txt'

# Save the first half to a new file with header
with open(first_half_path, 'w') as file:
    file.write(header)
    for sublist in first_half:
        file.write('\t'.join(map(str, sublist)) + '\n')

# Save the second half to a new file with header
with open(second_half_path, 'w') as file:
    file.write(header)
    for sublist in second_half:
        file.write('\t'.join(map(str, sublist)) + '\n')

print("First half saved to:", first_half_path)
print("Second half saved to:", second_half_path)


def browse_file(label_text, var, data_list):
    file_path = filedialog.askopenfilename(
        initialdir=r'C:\Users\plangner\OneDrive - IREC-edu\00 - PhD\00 - Samples',
        title=f"Select {label_text}",
        filetypes=(("Text files", "*.txt"), ("all files", "*.*"))
    )
    var.set(file_path)

    # Read and store data in the specified list
    if file_path:
        with open(file_path, 'r') as file:
            # Skip the header
            next(file)
            # Read and store the data in the list
            data_list.clear()
            for line in file:
                data_list.append(line.strip().split('\t'))


# Create the main window
root = tk.Tk()
root.title("File Selection")

# Variables to store file paths and data
potentiation_file_path_var = tk.StringVar()
depression_file_path_var = tk.StringVar()

potentiation_data = []
depression_data = []

# Instruction labels
instruction_label1 = tk.Label(root, text="First select file with potentiation pulses.")
instruction_label1.pack(pady=5)

instruction_label2 = tk.Label(root, text="Then select file with depression pulses.")
instruction_label2.pack(pady=5)


def calculate_asymmetric_ratio():
    # Check if both files are selected
    if potentiation_data and depression_data:
        # Initialize lists to store maximum differences for each value
        max_differences = [0.0] * 4  # Assuming there are four values (Conductivity, Delta Conductivity, Averaged Conductance, Delta Conductance)

        # Calculate the asymmetric ratio
        asymmetric_ratios = []
        for i in range(len(potentiation_data)):
            potentiation_values = [float(value) for value in potentiation_data[i][1:]]
            depression_values = [float(value) for value in depression_data[i][1:]]

            # Calculate the absolute difference for each value
            differences = [abs(potentiation - depression) for potentiation, depression in zip(potentiation_values, depression_values)]

            # Update the maximum differences for each value
            max_differences = [max(max_diff, diff) for max_diff, diff in zip(max_differences, differences)]

        # Calculate the asymmetric ratios using the maximum differences
        asymmetric_ratios = [max_diff / (abs(float(potentiation_data[-1][index + 1])) - abs(float(depression_data[-1][index + 1])))
                             for index, max_diff in enumerate(max_differences)]

        # Print the calculated asymmetric ratios
        print("Maximum Differences:", max_differences)
        print("Asymmetric Ratios:", asymmetric_ratios)


def select_files():
    browse_file("potentiation pulses", potentiation_file_path_var, potentiation_data)
    if potentiation_file_path_var.get():
        print("Selected potentiation pulses file:", potentiation_file_path_var.get())
        print("Potentiation data:", potentiation_data)

        browse_file("depression pulses", depression_file_path_var, depression_data)
        if depression_file_path_var.get():
            print("Selected depression pulses file:", depression_file_path_var.get())
            print("Depression data:", depression_data)

            # Calculate asymmetric ratios
            calculate_asymmetric_ratio()

            root.destroy()  # Close the main window if both files are selected


# Button for selecting both files
select_files_button = tk.Button(root, text="Select Files", command=select_files)
select_files_button.pack(pady=10)

# Run the main loop
root.mainloop()
