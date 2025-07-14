import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilenames, askdirectory

# Ask user to select input files
root = Tk()
root.withdraw()
filepaths = askopenfilenames(initialdir='C:/Users/plangner/OneDrive - IREC-edu/00 - PhD/00 - Samples', title='Select Files')
if not filepaths:
    print("No files selected. Program terminated.")
    exit()

# Ask user to select output directory
output_dir = askdirectory(initialdir=filepaths[0])
if not output_dir:
    print("No directory selected. Program terminated.")
    exit()

nyquist_data = []
bode_data = []

# Loop through all selected files
for filepath in filepaths:
    # Read data from CSV file
    data = np.genfromtxt(filepath, delimiter=' ', skip_header=1)

    # Extract columns
    f = data[:, 0].astype(float)
    zre = data[:, 1].astype(float)
    zim = data[:, 2].astype(float)
    # amp = data[:, 3].astype(float)
    # phase = data[:, 4].astype(float)
    # temperature = data[:, 5].astype(float)

    # Create DataFrame and save to TXT file
    df = pd.DataFrame({
        'Frequency': f,
        'Real': zre,
        'Imaginary': zim,
        # 'Amplitude': amp,
        # 'Phase': phase,
        # 'Temperature': temperature
    })
    txt_path = os.path.join(output_dir, os.path.splitext(os.path.basename(filepath))[0] + '.txt')
    df.to_csv(txt_path, index=False, header=False, sep='\t')

    # Create Nyquist plot and save to PNG file
    fig, ax = plt.subplots()
    ax.plot(zre, -zim)
    ax.set_xlabel('Real')
    ax.set_ylabel('-Imaginary')
    ax.set_title('Nyquist Plot')
    png_path = os.path.join(output_dir, os.path.splitext(os.path.basename(filepath))[0] + '_nyquist.png')
    plt.savefig(png_path)
    plt.close()

    # Add data to list for final Nyquist plot
    nyquist_data.append((zre, zim))

    # Create Bode plot and save to PNG file
    #fig, ax = plt.subplots()
   # ax.plot(f, amp)
    #ax.set_xscale('log')
   # ax.set_xlabel('Frequency (Hz)')
   # ax.set_ylabel('Amplitude (V)')
   # ax.set_title('Bode Plot')
   # png_path = os.path.join(output_dir, os.path.splitext(os.path.basename(filepath))[0] + '_bode.png')
   # plt.savefig(png_path)
   # plt.close()

    # Add data to list for final Bode plot
   # bode_data.append((f, amp))

# Create final Nyquist plot with data from all selected files
fig, ax = plt.subplots()
cmap = plt.get_cmap('coolwarm')  # Choose a colormap

num_files = len(nyquist_data)
color_range = np.linspace(0, 1, num_files)  # Generate values for the color transition

for i, data in enumerate(nyquist_data):
    zre, zim = data
    filepath = filepaths[i]  # Get the corresponding filepath
    label = os.path.splitext(os.path.basename(filepath))[0]  # Extract the filename without extension

    color = cmap(color_range[i])  # Retrieve color from the colormap

    ax.plot(zre, -zim, label=label, color=color)

ax.set_xlabel('Real')
ax.set_ylabel('-Imaginary')
ax.set_title('Nyquist Plot - All Files')
ax.legend()
png_path = os.path.join(output_dir, 'nyquist_all.png')
plt.savefig(png_path)
plt.close()

# Create final Bode plot with data from all selected files
#fig, ax = plt.subplots()
#for i, data in enumerate(bode_data):
 #   f, amp = data
 #   ax.plot(f, amp, label=os.path.splitext(os.path.basename(filepath))[0])
 #   ax.set_xscale('log')
 #   ax.set_xlabel('Frequency (Hz)')
  # ax.set_ylabel('Amplitude (V)')
 #   ax.set_title('Bode Plot - All Files')
#    ax.legend()
#png_path = os.path.join(output_dir, 'bode_all.png')
#plt.savefig(png_path)
#plt.close()