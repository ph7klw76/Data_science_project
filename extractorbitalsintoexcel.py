import pandas as pd
import os

def extract_lumo_extended(file_contents):
    """
    Extracts the HOMO, LUMO, HOMO-1, HOMO-2, LUMO+1, and LUMO+2 data from the given file content.
    """
    lines = file_contents.split("\n")
    homo = lumo = homo_1 = homo_2 = lumo_1 = lumo_2 = None
    occ_2_counter = 0
    occ_0_counter = 0

    for line in lines:
        parts = line.split()
        if len(parts) == 4:
            occ = parts[1]
            e_ev = parts[3]

            if occ == '2.0000':
                occ_2_counter += 1
                if occ_2_counter == 1:
                    homo = e_ev
                elif occ_2_counter == 2:
                    homo_1 = e_ev
                elif occ_2_counter == 3:
                    homo_2 = e_ev

            elif occ == '0.0000':
                occ_0_counter += 1
                if occ_0_counter == 1:
                    lumo = e_ev
                elif occ_0_counter == 2:
                    lumo_1 = e_ev
                elif occ_0_counter == 3:
                    lumo_2 = e_ev

    return lumo, lumo_1, lumo_2

def extract_homo_extended(file_contents):
    """
    Extracts the HOMO, HOMO-1, HOMO-2, LUMO, LUMO+1, and LUMO+2 data from the given file content.
    """
    lines = file_contents.split("\n")
    orbitals = []
    for line in lines:
        parts = line.split()
        if len(parts) == 4:
            occ = parts[1]
            e_ev = parts[3]
            orbitals.append((occ, e_ev))

    # Reverse the list to find HOMO (last 2.0000), HOMO-1 (second last 2.0000), and HOMO-2 (third last 2.0000)
    orbitals.reverse()

    homo = homo_1 = homo_2 = None
    occ_2_counter = 0

    for occ, e_ev in orbitals:
        if occ == '2.0000':
            occ_2_counter += 1
            if occ_2_counter == 1:
                homo = e_ev
            elif occ_2_counter == 2:
                homo_1 = e_ev
            elif occ_2_counter == 3:
                homo_2 = e_ev

    return homo, homo_1, homo_2

def extract_lumo_extended_from_file(file_path):
    """
    Reads the file and extracts the HOMO, LUMO, HOMO-1, HOMO-2, LUMO+1, and LUMO+2 data.
    """
    with open(file_path, 'r') as file:
        file_contents = file.read()
    lumo, lumo_1, lumo_2=extract_lumo_extended(file_contents)
    return lumo, lumo_1, lumo_2

def extract_homo_extended_from_file(file_path):
    """
    Reads the file and extracts the HOMO, LUMO, HOMO-1, HOMO-2, LUMO+1, and LUMO+2 data.
    """
    with open(file_path, 'r') as file:
        file_contents = file.read()
    homo, homo_1, homo_2=extract_homo_extended(file_contents)
    return homo, homo_1, homo_2

def update_excel_with_orbitals(file_path, excel_file_path):
    # Extract HOMO, HOMO-1, HOMO-2, LUMO, LUMO+1, and LUMO+2 from the provided file
    lumo, lumo_1, lumo_2 = extract_lumo_extended_from_file(file_path)
    homo, homo_1, homo_2 = extract_homo_extended_from_file(file_path)

    # Load existing Excel file
    df = pd.read_excel(excel_file_path)

    # Extract filename without extension for matching
    Filename = file_path.split('/')[-1].split('.')[0]  # Extract filename without extension

    # Check if 'filename' column exists
    if 'Filename' not in df.columns:
        print("The Excel file does not have a 'filename' column.")
        return

    # Find the row in the dataframe that matches the filename
    if Filename in df['Filename'].values:
        row_index = df[df['Filename'] == Filename].index
        # Update the dataframe with new data
        df.loc[row_index, ['HOMO', 'HOMO-1', 'HOMO-2', 'LUMO', 'LUMO+1', 'LUMO+2']] = [homo, homo_1, homo_2, lumo, lumo_1, lumo_2]
    else:
        print(f"Filename '{Filename}' not found in the Excel file.")

    # Save the updated dataframe back to the Excel file
    df.to_excel(excel_file_path, index=False)

def process_directory(directory_path, excel_file_path):
    """
    Processes all .out files in a given directory and updates the Excel file with orbital data.
    """
    for filename in os.listdir(directory_path):
        if filename.endswith(".out"):
            file_path = os.path.join(directory_path, filename)
            update_excel_with_orbitals(file_path, excel_file_path)

# File path to the input file
directory_path = 'D:/OSC/file/'
excel_file_path = 'D:/labkicosmos/ML3/updated_combined_data.xlsx'
process_directory(directory_path, excel_file_path)
