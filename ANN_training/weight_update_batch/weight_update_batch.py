import os
from tkinter import Tk, filedialog

def process_data(input_file):
    with open(input_file, 'r') as file:
        # Read and parse the header
        header = file.readline().strip().split('\t')

        # Add two new columns to the header
        header.extend(["Cond PP (S/cm)", "G per pulse (S)"])

        # Read the data
        data = [line.strip().split('\t') for line in file]

        # Initialize previous values for conductivity and conductance
        prev_cond = float(data[0][1])
        prev_g = float(data[0][3])

        # Process and add new columns
        for row in data:
            cond_diff = float(row[1]) - prev_cond
            g_diff = float(row[3]) - prev_g

            # Append new values to the row
            row.extend([cond_diff, g_diff])

            # Update previous values for the next iteration
            prev_cond = float(row[1])
            prev_g = float(row[3])

    # Write the processed data back to the file
    output_file = input_file.replace(".txt", "_processed.txt")
    with open(output_file, 'w') as output:
        # Write the header
        output.write('\t'.join(header) + '\n')

        # Write the processed data
        for row in data:
            output.write('\t'.join(map(str, row)) + '\n')

    print(f"Processed data written to {output_file}")

def select_files():
    root = Tk()
    root.withdraw()  # Hide the main window

    initial_dir = r'C:\Users\plangner\OneDrive - IREC-edu\00 - PhD\00 - Samples'
    file_paths = filedialog.askopenfilenames(initialdir=initial_dir, title="Select .txt files",
                                             filetypes=(("Text files", "*.txt"), ("All files", "*.*")))

    if not file_paths:
        print("No files selected.")
        return None

    print(f"Selected files: {file_paths}")
    return file_paths

if __name__ == "__main__":
    # Ask the user to select multiple files using the file dialog
    selected_files = select_files()

    if selected_files:
        # Process each selected file
        for file in selected_files:
            process_data(file)
