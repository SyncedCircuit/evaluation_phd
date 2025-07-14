import tkinter as tk


# Define constants
OHM_PER_S = 1.0
MICROMETER = 1e-4
NANOMETER = 1e-7

# Define function to calculate conductivity
def calculate_conductivity():
    resistance = float(resistance_entry.get())
    length = float(length_entry.get())
    width = float(width_entry.get())
    thickness = float(thickness_entry.get())
    units = unit_dropdown.get()

    # Convert units to meters
    if units == "micrometer":
        length *= MICROMETER
        width *= MICROMETER
        thickness *= MICROMETER
    elif units == "nanometer":
        length *= NANOMETER
        width *= NANOMETER
        thickness *= NANOMETER

    # Calculate conductivity in S/cm
    conductivity = (OHM_PER_S / resistance) * (length / (width * thickness))
    # Calculate conductance in S
    conductance = 1 / resistance

    # Update output label
    output_label.config(text="Conductivity: {:.2e} S/cm, Conductance: {:.2e} S".format(conductivity, conductance))

# Create GUI window
root = tk.Tk()
root.title("Conductivity Calculator")

# Create input fields
length_label = tk.Label(root, text="Length (L):")
length_label.grid(row=0, column=0, padx=5, pady=5)
length_entry = tk.Entry(root)
length_entry.grid(row=0, column=1, padx=5, pady=5)

width_label = tk.Label(root, text="Width (w):")
width_label.grid(row=1, column=0, padx=5, pady=5)
width_entry = tk.Entry(root)
width_entry.grid(row=1, column=1, padx=5, pady=5)

thickness_label = tk.Label(root, text="Thickness (t):")
thickness_label.grid(row=2, column=0, padx=5, pady=5)
thickness_entry = tk.Entry(root)
thickness_entry.grid(row=2, column=1, padx=5, pady=5)

unit_label = tk.Label(root, text="Unit:")
unit_label.grid(row=3, column=0, padx=5, pady=5)
unit_dropdown = tk.StringVar(root)
unit_dropdown.set("micrometer")
unit_menu = tk.OptionMenu(root, unit_dropdown, "micrometer", "nanometer")
unit_menu.grid(row=3, column=1, padx=5, pady=5)

resistance_label = tk.Label(root, text="Resistance (Ohm):")
resistance_label.grid(row=4, column=0, padx=5, pady=5)
resistance_entry = tk.Entry(root)
resistance_entry.grid(row=4, column=1, padx=5, pady=5)

# Load and display image
image_file = r"C:\Users\plangner\OneDrive - IREC-edu\00 - PhD\13 - Pictures\Geometry EGT_2.png"
image = tk.PhotoImage(file=image_file)
image_label = tk.Label(root, image=image)
image_label.grid(row=0, column=2, rowspan=5, padx=5, pady=5)

# Create formula label
formula_label = tk.Label(root, text="Conductivity (σ) = (L / (w * t)) / R", font=("Arial", 14))
formula_label.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

# Create calculate button
calculate_button = tk.Button(root, text="Calculate", command=calculate_conductivity)
calculate_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Create output label
output_label = tk.Label(root, text="")
output_label.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
