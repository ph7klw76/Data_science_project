def extract_all_final_single_point_energy(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # Reverse the lines for easier search from the bottom
        lines = lines[::-1]

        extracted_strings = []
        last_final_single_point_energy = ""
        for i, line in enumerate(lines):
            if "*** OPTIMIZATION RUN DONE ***" in line:
                # Check if there are at least three lines before this line
                if i + 3 < len(lines):
                    extracted_strings.append(lines[i + 3].strip())
            if "FINAL SINGLE POINT ENERGY" in line and last_final_single_point_energy == "":
                last_final_single_point_energy = line.strip()
                
        return extracted_strings, last_final_single_point_energy
    except Exception as e:
        return [f"Error: {e}"], ""

file_path="D:/OSC/file/test/143-a-3BNMes.out"
extracted_strings, last_final_energy = extract_all_final_single_point_energy(file_path)
print(extracted_strings, last_final_energy)
