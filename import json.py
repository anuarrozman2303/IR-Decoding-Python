## Version Date : 19/5/2023
# Fixed section = "temp" json formatted command.                        #Done
# Reworked codes to be dynamic.                                         #Done
## Version Date : 22/5/2023
# Fixed files content didnt filtered before comparing process.          #Done
# Fixed commands each function are correct.                             #Done
## Task Date : 23/5/2023
# Combining setTo0 and setToVal commands together.                      #Done
# import lists.py (ir protocol config file)                             #Done
# Combining commands of similar hexpos with based on their files name.  #
# Adding more device informations.                                      #Done

import configparser
import re
from lists import *

HEXPOS_GROUP_SIZE = 8
HEXPOS_TO_EXCLUDE = chsum_address

def filter_file_content(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        # Filter process
        for i in range(len(lines)):
            lines[i] = lines[i].split(':', 1)[-1]
            lines[i] = ''.join([c for c in lines[i] if c.isdigit()])
        # Remove empty lines & move up the data.
        lines = [line.strip() for line in lines if line.strip()]
        return lines

def compare_files(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()

        # Compare lines
        diff_lines = []
        for line_num, (line1, line2) in enumerate(zip(lines1, lines2), start=1):
            if line1.strip() != line2.strip():
                diff_lines.append((line_num, line1.strip(), line2.strip()))
        return diff_lines

def setToZero(file_path, hexpos):
    output = '{"name":"' + file_path + '",inst:'
    
    hexpos_dict = combined_line_nums.get(section, {})
    hexpos_line_nums = hexpos_dict.get(hexpos, [])
    
    combined_line_nums_set = sorted(set(hexpos_line_nums))
    pos_values = [num % HEXPOS_GROUP_SIZE for num in combined_line_nums_set]
    
    if all(pos in range(1, 5) for pos in pos_values):
        output += f'[[{hexpos},15,12],'
    elif any(pos in [5, 6, 7, 0] for pos in pos_values) and not any(pos in [1, 2, 3, 4] for pos in pos_values):
        output += f'[[{hexpos},240,12],'
    else:
        output += f'[[{hexpos},255,12],'
    return output

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the config file
config.read('config.ini')

# Dictionary to store combined line_nums for each hexpos in each section
combined_line_nums = {}
# List to store filtered content of each file
filtered_file_paths = set()


# Iterate over sections
for section in config.sections():
    file_list = [config.get(section, option) for option in config.options(section)]
    file_count = len(file_list)
    printed_combinations = set()

    if section != "temp":
        # Filter files and store the filtered content
        filtered_content = [filter_file_content(file_path) for file_path in file_list]
        filtered_file_paths.update(file_list)

        # Overwrite the files with the filtered content
        for file_path, filtered_content in zip(file_list, filtered_content):
            with open(file_path, 'w') as f:
                f.write('\n'.join(filtered_content))

        # Compare files
        diff_lines_dict = {}  # Dictionary to store the diff_lines for each file_path
        for i in range(file_count - 1):
            file1_path = file_list[i]
            file2_path = file_list[i + 1]
            diff_lines = compare_files(file1_path, file2_path)
            if diff_lines:
                diff_lines_dict[file1_path] = diff_lines

        # Print the grouped output
        # Print remaining files that were not compared
        for file_path in filtered_file_paths:
            if file_path not in printed_combinations:
                with open(file_path, "r") as f:
                    file_lines = f.readlines()
                    hex_sequence = file_lines[:HEXPOS_GROUP_SIZE]
                    characters = (''.join(hex_sequence).replace('\n', '')[::-1])
                    characters_int = int(characters, 2)  # Convert characters to an integer
                    printed_combinations.add(file_path)
                    output = setToZero(file_path, 1)
                    print(output, end='')
                    print(f'[{1},{characters_int},13]')


                for hexpos, lines in hexpos_lines.items():
                    if section not in combined_line_nums:
                        combined_line_nums[section] = {}
                    if hexpos not in combined_line_nums[section]:
                        combined_line_nums[section][hexpos] = []
                    combined_line_nums[section][hexpos].extend([line_num for line_num, _, _ in lines])

                    combination = f"{file_path}:{hexpos}"
                    if combination not in printed_combinations:
                        with open(file_path, "r") as f:
                            file_lines = f.readlines()
                            start_line = (hexpos - 1) * HEXPOS_GROUP_SIZE
                            end_line = start_line + HEXPOS_GROUP_SIZE
                            hex_sequence = file_lines[start_line:end_line]
                            characters = (''.join(hex_sequence).replace('\n', '')[::-1])
                            characters_int = int(characters, 2)  # Convert characters to an integer
                            printed_combinations.add(combination)
                            output = setToZero(file_path, hexpos)
                            print(output, end='')
                            print(f'[{hexpos},{characters_int},13]')
                        hexpos_lines[hexpos] = []
            else:
                if section not in combined_line_nums:
                    combined_line_nums[section] = {}
                combined_line_nums[section][1] = []

# Print remaining files that were not compared
for file_path in filtered_content_list:
    if file_path not in printed_combinations:
        with open(file_path, "r") as f:
            file_lines = f.readlines()
            hex_sequence = file_lines[:HEXPOS_GROUP_SIZE]
            characters = (''.join(hex_sequence).replace('\n', '')[::-1])
            characters_int = int(characters, 2)  # Convert characters to an integer
            printed_combinations.add(file_path)
            output = setToZero(file_path, 1)
            print(output, end='')
            print(f'[{1},{characters_int},13]')