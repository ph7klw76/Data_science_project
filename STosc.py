import os
import pandas as pd

def extract_energy(file):
    singlets = []
    triplets = []
    oscillator_strengths = []

    with open(file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 7:  # Skip lines that don't have enough data
                continue

            if 'singlet' in line:
                energy = float(parts[4])
                osc_strength = float(parts[6]) if 'singlet' in parts else 0.0
                singlets.append(energy)
                oscillator_strengths.append(osc_strength)
            elif 'triplet' in line:
                energy = float(parts[4])
                triplets.append(energy)

    # Getting the filename without the extension
    filename_without_extension = os.path.splitext(os.path.basename(file))[0]

    # Creating a DataFrame
    max_length = max(len(singlets), len(triplets))
    data = {
        'Filename': [filename_without_extension] * max_length,
        'Singlets': singlets + [None] * (max_length - len(singlets)),
        'Triplets': triplets + [None] * (max_length - len(triplets)),
        'Oscillator Strengths': oscillator_strengths + [None] * (max_length - len(oscillator_strengths))
    }
    return pd.DataFrame(data)

# Directory containing the .out files
directory = 'D:/test/'

# DataFrame to hold all data
all_data = pd.DataFrame()

# Loop through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.log'):
        file_path = os.path.join(directory, filename)
        df = extract_energy(file_path)
        all_data = all_data.append(df, ignore_index=True)

# Save the combined data to an Excel file
all_data.to_excel('D:/test/combined_data.xlsx', index=False)

print("Data extraction complete. Saved to 'combined_data.xlsx'")


