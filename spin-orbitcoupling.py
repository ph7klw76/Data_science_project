import pandas as pd
import os

def extract_data_from_file(file_path):
    """
    Extracts specific data from a text file and saves it in an Excel file.
    """
    # Reading data from the file
    with open(file_path, 'r') as file:
        data = file.read()

    # Extracting specific data
    extracted_data = {}
    for line in data.strip().split('\n'):
        key, value = line.split(':')
        key = key.strip()
        value = float(value.strip())
        if key in ["Root ('1', '1')", "Root ('2', '1')"]:
            extracted_data[key] = value

    # Creating a DataFrame
    df = pd.DataFrame({
        'T1S1': [extracted_data.get("Root ('1', '1')", None)],
        'T2S1': [extracted_data.get("Root ('2', '1')", None)]
    })

    # Define the output Excel file path
    output_file_path = file_path.replace('.txt', '_extracted.xlsx')

    # Saving to Excel
    df.to_excel(output_file_path, index=False)

    return output_file_path

def process_all_txt_files_in_folder(folder_path):
    """
    Processes all .txt files in a specified folder.
    """
    output_files = []

    # Iterating over all files in the given folder
    for file in os.listdir(folder_path):
        if file.endswith('.txt'):
            file_path = os.path.join(folder_path, file)
            output_file_path = extract_data_from_file(file_path)
            output_files.append(output_file_path)

    return output_files

# Example usage
folder_path = 'path/to/your/folder'  # Replace with the actual path to your folder
processed_files = process_all_txt_files_in_folder(folder_path)

print(processed_files)
