import json
import re
# Define data structure to hold singlets and triplets
singlets = []
triplets = []
delta_E=[]
pattern = r"/lustre/user/woon/labkicosmos/ML2/(.*).ts"
# Read the data from a text file named 'energy_data.txt'
with open('D:\labkicosmos\energy.out', 'r') as f:
    lines = f.readlines()

# Process each line to extract relevant information
for line in lines:
    match = re.search(pattern, line)
    if match:
        extracted_text = match.group(1)
    # Remove leading and trailing whitespaces and split by spaces
    parts = line.strip().split() 
    # Check if the line contains the required number of fields (at least 8 fields)
    if len(parts)==7 and parts[0].isdigit():
        if parts[1]=='triplet' or parts[1]=='singlet':
            # Extract root, multiplicity, energy in eV and oscillatory strength
            root = int(parts[0])
            multiplicity = parts[1]
            energy_eV = float(parts[4])
            osc_strength = float(parts[6])   
            # Store singlets and triplets in their respective lists
            if multiplicity == 'singlet':
                singlets.append({
                    'molecule':extracted_text,
                    'root': root,
                    'energy_eV': energy_eV,
                    'osc_strength': osc_strength
                })
            elif multiplicity == 'triplet':
                triplets.append({
                    'molecule':extracted_text,
                    'root': root,
                    'energy_eV': energy_eV,
                    'osc_strength': osc_strength
                })

# Display the extracted information
print("Singlets:")
for entry in singlets:
    print(f"Root: {entry['root']}, Energy (eV): {entry['energy_eV']}, Oscillatory Strength: {entry['osc_strength']}")

print("\nTriplets:")
for entry in triplets:
    print(f"Root: {entry['root']}, Energy (eV): {entry['energy_eV']}, Oscillatory Strength: {entry['osc_strength']}")

with open('singlets.json', 'w') as f:
    json.dump(singlets, f, indent=4)

with open('triplets.json', 'w') as f:
    json.dump(triplets, f, indent=4)

# Optionally, display that the data has been saved
print("Data has been saved to 'singlets.json' and 'triplets.json'.")

with open('singlets.json', 'r') as f:
    data_singlet = json.load(f)
with open('triplets.json', 'r') as f2:
    data_triplets = json.load(f2)

# Iterate over the data to find entries with root: 3 and print their energy_eV
for entry in data_singlet:
    if entry['root'] == 3:
        molecule = entry['molecule']
        energy_eV = entry['energy_eV']
        for entry2 in data_triplets:
            if entry2['root'] == 2 and entry2['molecule']==molecule:
                energy_eV2 = entry2['energy_eV']
            if entry2['root'] == 4 and entry2['molecule']==molecule:
                energy_eV3 = entry2['energy_eV']
                delta_E.append({"molecule":molecule,
                                "delta_ES1_T1":float(energy_eV)-float(energy_eV2),
                                "delta_ET2_S1":float(energy_eV3)-float(energy_eV)
                                })
with open('deltaE.json', 'w') as f:
    json.dump(delta_E, f, indent=4)
