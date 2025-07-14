import os
import csv
import matplotlib.pyplot as plt
from tkinter import Tk, simpledialog, messagebox, Label, Entry, Button
from tkinter.filedialog import askopenfilenames, askdirectory
from PIL import Image, ImageTk

# Create a Tkinter root window
root = Tk()
root.title("Threshold Selection and Parameters")
root.geometry("800x400")

# Function to handle button click
def process_files():
    # Get the threshold column header entered by the user
    threshold_column = threshold_entry.get()

    # Get the length, width, and thickness values entered by the user
    length = float(length_entry.get())
    width = float(width_entry.get())
    thickness = float(thickness_entry.get())

    # Ask the user to select input CSV files
    filepaths = askopenfilenames(initialdir='C:/Users/plangner/OneDrive - IREC-edu/00 - PhD/00 - Samples', title='Select CSV Files')
    if not filepaths:
        messagebox.showinfo("Error", "No files selected. Program terminated.")
        return

    # Ask the user to select the output directory
    output_dir = askdirectory(initialdir=os.path.dirname(filepaths[0]))
    if not output_dir:
        messagebox.showinfo("Error", "No directory selected. Program terminated.")
        return

    # Prompt the user to enter the threshold value
    threshold_value = simpledialog.askfloat("Threshold Value for Pulse Detection", f"Enter the amplitude value of applied pulses [in V or A] (in rawdata column {threshold_column})")

    # Iterate over the selected input CSV files and save them as tab-separated text files
    for filepath in filepaths:
        # Extract the file name without extension
        file_name = os.path.splitext(os.path.basename(filepath))[0]

        # Define the raw data file path
        raw_data_file = os.path.join(output_dir, file_name + "_raw_data.txt")

        # Read the input CSV file
        with open(filepath, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)

        # Calculate the conductivity and conductance values
        resistance_column = "CHRES"
        resistance_index = data[0].index(resistance_column)
        data[0].append("Conductivity (S/cm)")
        data[0].append("Conductance (S)")

        for row in data[1:]:
            resistance = float(row[resistance_index].replace(',', '.'))

            # Convert units to meters
            length_meters = length / 1e4  # Convert length from micrometers to centimeters
            width_meters = width / 1e4  # Convert width from micrometers to centimeters
            thickness_meters = thickness / 1e4  # Convert thickness from micrometers to centimeters

            conductivity = (1 / resistance) * (length_meters / (width_meters * thickness_meters))
            row.append(f"{conductivity:.3e}")

            conductance = (1 / resistance)
            row.append(f"{conductance:.3e}")

        # Write the CSV data to the output TXT file in tab-separated format
        with open(raw_data_file, 'w', newline='') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerows(data)

        print(f"Raw data file saved as '{raw_data_file}'.")

    # Perform pulse detection and averaging
    combined_conductivity_data = []
    combined_conductance_data = []

    for filepath in filepaths:
        # Extract the file name without extension
        file_name = os.path.splitext(os.path.basename(filepath))[0]

        # Open the input TXT file
        with open(os.path.join(output_dir, file_name + "_raw_data.txt"), 'r') as file:
            reader = csv.reader(file, delimiter='\t')
            data = list(reader)

        # Extract the header row and data rows
        header = data[0]
        rows = data[1:]

        # Convert the values in the threshold column to positive absolute values
        threshold_column_index = header.index(threshold_column)
        threshold_values = [abs(float(row[threshold_column_index].replace(',', '.'))) for row in rows]

        # Calculate the adjusted threshold value
        adjusted_threshold_value = abs(threshold_value) - abs(threshold_value) * 0.1

        # Initialize lists for conductivity and conductance data
        conductivity_values = []
        conductance_values = []  # store averaged conductance values
        pulses = []
        pulse_count = -1
        prev_value = None  # to store the previous row's value
        initial_conductivity = None  # store the initial pulse's conductivity
        initial_conductance = None  # store the initial pulse's conductance

        for row, value in zip(rows, threshold_values):
            if value > adjusted_threshold_value:
                if prev_value is not None and prev_value > adjusted_threshold_value:
                    # Previous row's value was higher than the threshold, don't increase pulse_count
                    pass
                else:
                    pulse_count += 1

                if conductivity_values:
                    conductivity_avg = sum(conductivity_values) / len(conductivity_values)
                    conductance_avg = sum(conductance_values) / len(conductance_values)
                    delta_conductivity = (
                        0.0 if initial_conductivity is None else conductivity_avg - initial_conductivity
                    )
                    delta_conductance = (
                        0.0 if initial_conductance is None else conductance_avg - initial_conductance
                    )
                    pulses.append(
                        (pulse_count, conductivity_avg, delta_conductivity, conductance_avg, delta_conductance))
                    conductance_values.append(conductance_avg)

                # Set initial conductivity and conductance for the first pulse
                if initial_conductivity is None:
                    initial_conductivity = conductivity_avg
                if initial_conductance is None:
                    initial_conductance = conductance_avg

                conductivity_values.clear()
                conductance_values.clear()
            else:
                conductivity_value = float(row[header.index("Conductivity (S/cm)")])
                conductivity_values.append(conductivity_value)

                # Calculate conductance and add to conductance_values
                resistance_value = float(row[header.index("CHRES")].replace(',', '.'))
                conductance = 1 / resistance_value
                conductance_values.append(conductance)

            prev_value = value  # Update prev_value for the next iteration

        # Add the last detected pulse if conductivity_values exist after the last row
        if conductivity_values:
            pulse_count += 1
            conductivity_avg = sum(conductivity_values) / len(conductivity_values)
            conductance_avg = sum(conductance_values) / len(conductance_values)
            delta_conductivity = 0.0 if initial_conductivity is None else conductivity_avg - initial_conductivity
            delta_conductance = 0.0 if initial_conductance is None else conductance_avg - initial_conductance
            pulses.append((pulse_count, conductivity_avg, delta_conductivity, conductance_avg, delta_conductance))

        # Define the pulse list file path
        pulse_list_file = os.path.join(output_dir, file_name + "_pulse_list.txt")

        # Write the pulse list to the output TXT file
        with open(pulse_list_file, 'w', newline='') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerow(["Pulse Number", "Conductivity (S/cm)", "Delta Conductivity (S/cm)", "Conductance (S)", "Delta Conductance (S)"])
            writer.writerows(pulses)

        print(f"Pulse list generated. Pulse list file saved as '{pulse_list_file}'.")
        print(pulses)

        # Extract pulse numbers, conductivity values, delta EPSC values, and averaged conductance values
        pulse_numbers, conductivity_values, delta_conductivity_values, conductance_values, delta_conductance_values = zip(*pulses)

        # Append data to combined conductivity and conductance lists
        combined_conductivity_data.append((pulse_numbers, conductivity_values))
        combined_conductance_data.append((pulse_numbers, conductance_values))


    # Remove empty rows from pulse list files
    for filepath in filepaths:
        # Extract the file name without extension
        file_name = os.path.splitext(os.path.basename(filepath))[0]

        # Define the pulse list file path
        pulse_list_file = os.path.join(output_dir, file_name + "_pulse_list.txt")

        # Read the pulse list file
        with open(pulse_list_file, 'r') as file:
            reader = csv.reader(file, delimiter='\t')
            pulse_data = list(reader)

        # Remove empty rows
        pulse_data = [row for row in pulse_data if any(row)]

        # Write the pulse list to the output TXT file
        with open(pulse_list_file, 'w', newline='') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerows(pulse_data)

        # print(f"Empty rows removed from '{pulse_list_file}'.")

    # Generate the combined graph
    plt.figure()

    # Plot conductivity
    for i, data in enumerate(combined_conductivity_data):
        pulse_numbers, conductivity_values = data
        file_name = os.path.splitext(os.path.basename(filepaths[i]))[0]
        plt.plot(pulse_numbers, conductivity_values, label=f"{file_name} - Conductivity")

    plt.xlabel('Pulse Number')
    plt.ylabel('Conductivity (S/cm)')
    plt.title('Conductivity Graph')
    plt.legend()
    plt.savefig(os.path.join(output_dir, "conductivity_graph.png"), format='png')
    plt.show()

    plt.figure()

    # Plot conductance
    for i, data in enumerate(combined_conductance_data):
        pulse_numbers, conductance_values = data
        file_name = os.path.splitext(os.path.basename(filepaths[i]))[0]
        plt.plot(pulse_numbers, conductance_values, label=f"{file_name} - Conductance")

    plt.xlabel('Pulse Number')
    plt.ylabel('Conductance (S)')
    plt.title('Conductance Graph')
    plt.legend()
    plt.savefig(os.path.join(output_dir, "conductance_graph.png"), format='png')
    plt.show()

    print("Conductivity and Conductance graphs generated.")

# Create labels and entry fields for threshold column, length, width, and thickness
threshold_label = Label(root, text="Pulses Column Header:")
threshold_label.grid(row=0, column=0, sticky="w")
threshold_entry = Entry(root)
threshold_entry.grid(row=0, column=1)

length_label = Label(root, text="Length L [µm]:")
length_label.grid(row=1, column=0, sticky="w")
length_entry = Entry(root)
length_entry.grid(row=1, column=1)

width_label = Label(root, text="Width W [µm]:")
width_label.grid(row=2, column=0, sticky="w")
width_entry = Entry(root)
width_entry.grid(row=2, column=1)

thickness_label = Label(root, text="Thickness th [µm]:")
thickness_label.grid(row=3, column=0, sticky="w")
thickness_entry = Entry(root)
thickness_entry.grid(row=3, column=1)

# Create the equation label
equation_label = Label(root, text="σ = (L/(W*th))/R")
equation_label.grid(row=4, column=0, columnspan=2, sticky="nsew")

# Create button to process the files
process_button = Button(root, text="Process Files", command=process_files)
process_button.grid(row=5, column=0, columnspan=2)

# Load and display the image if it exists
image_path = "C:/Users/plangner/OneDrive - IREC-edu/00 - PhD/13 - Pictures/Geometry EGT_2.png"
if os.path.isfile(image_path):
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)
    image_label = Label(root, image=photo)
    image_label.image = photo
    image_label.grid(row=0, column=2, rowspan=6, sticky="nsew")

    # Calculate the size of the image
    image_width = image.width
    image_height = image.height

    # Adjust the window size to fit the image
    window_width = image_width + 400  # Adjust as needed
    window_height = max(image_height, 400)  # Adjust as needed
    root.geometry(f"{window_width}x{window_height}")
else:
    print("Image not found.")

# Start the Tkinter event loop
root.mainloop()
