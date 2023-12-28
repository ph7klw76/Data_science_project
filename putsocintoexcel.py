import pandas as pd
excel_path = 'D:/labkicosmos/ML3/combined_data.xlsx'
excel_df = pd.read_excel(excel_path)

# Get the unique filenames from the first column
unique_filenames = excel_df['Filename'].unique()

# Dictionary to keep track of the data to be added to the DataFrame
data_to_add = {}

# List to keep track of missing files
missing_files = []

# Process each unique filename
for filename in unique_filenames:
    # Attempt to open the corresponding .txt file
    txt_file_path = f'D:/OSC/file/{filename}.txt'
    
    try:
        with open(txt_file_path, 'r') as file:
            # Read the content of the file
            content = file.read()
            
            # Search for the required roots in the file content
            root_1_1_search = "Root ('1', '1'): "
            root_2_1_search = "Root ('2', '1'): "
            
            # Find the positions of the required roots
            root_1_1_pos = content.find(root_1_1_search)
            root_2_1_pos = content.find(root_2_1_search)
            print
            
            # Extract the numbers after the found positions
            if root_1_1_pos != -1:
                root_1_1_value = content[root_1_1_pos + len(root_1_1_search):].split('\n', 1)[0]
                data_to_add[filename] = {'T1-S1': float(root_1_1_value)}
            if root_2_1_pos != -1:
                root_2_1_value = content[root_2_1_pos + len(root_2_1_search):].split('\n', 1)[0]
                if filename in data_to_add:
                    data_to_add[filename]['T2-S1'] = float(root_2_1_value)
                else:
                    data_to_add[filename] = {'T2-S1': float(root_2_1_value)}
    
    except FileNotFoundError:
        # Record the missing file
        missing_files.append(filename)

# Update the DataFrame with the new data
for filename, values in data_to_add.items():
    for key, value in values.items():
        excel_df.loc[excel_df['Filename'] == filename, key] = value

# Save the updated DataFrame to a new Excel file
updated_excel_path = 'D:/labkicosmos/ML3/updated_combined_data.xlsx'
excel_df.to_excel(updated_excel_path, index=False)

# Return the path to the updated Excel file and the list of missing files
updated_excel_path, missing_files
