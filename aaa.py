import os
import re
import configparser
import json
from lists import *

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

def compare_lines(line1, line2, excluded_hex_pos):
    if len(line1) != len(line2):
        return None
    diff_info = []
    for i in range(len(line1)):
        if line1[i] != line2[i]:
            hex_pos = i // 8 + 1  # Grouping every 8 characters as 1 hex_pos
            if hex_pos not in excluded_hex_pos:
                line_num = i + 1  # Adding 1 to get the line number
                diff_info.append((hex_pos, line_num))
    return diff_info

def extract_8_characters(filename, hex_pos, line_num):
    start_line = ((hex_pos - 1) * 8) + 1
    end_line = start_line + 7

    with open(filename, 'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines if line.strip()]
        lines = lines[start_line - 1: end_line]
        return ''.join(lines)

def generate_output(pos_str, hexpos):
    pos_list = [int(pos) for pos in pos_str.split(',')]  # Convert pos_str to a list of integers
    output = []
    if all(pos in range(1, 5) for pos in pos_list):
        output = [hexpos, 15, 12]
    elif any(pos in [5, 6, 7, 0] for pos in pos_list) and not any(pos in [1, 2, 3, 4] for pos in pos_list):
        output = [hexpos, 240, 12]
    else:
        output = [hexpos, 255, 12]
    return output

import json
import configparser
import os


def process_files_in_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)

    excluded_hex_pos = [8, 16, 35]  # List of excluded hex_pos values

    output = {}  # Dictionary to store output for each file_name
    for section in config.sections():
        filtered_files = {}

        # Filter files
        for key in config[section]:
            file_path = config[section][key]
            filtered_content = filter_file_content(file_path)
            filtered_files[key] = (filtered_content, file_path)

        # Compare filtered key-value pairs
        keys = list(filtered_files.keys())
        diff_info_by_section = {}  # Dictionary to store diff_info by section
        for i in range(len(keys)-1):
            key1 = keys[i]
            value1, file1 = filtered_files[key1]
            for j in range(i+1, len(keys)):
                key2 = keys[j]
                value2, file2 = filtered_files[key2]
                diff_info = compare_lines(value1, value2, excluded_hex_pos)
                if diff_info:
                    diff_info_by_section.setdefault(section, []).extend(diff_info)

        if section != "temp":
            
            # Combine unique line numbers by hex_pos for each section
            unique_lines_by_hex_pos = {}
            for hex_pos, line_num in diff_info_by_section.get(section, []):
                unique_lines_by_hex_pos.setdefault(hex_pos, set()).add(line_num)

            section_output = []
            for key, (filtered_content, file_path) in filtered_files.items():
                if key in config[section]:
                    commands = []
                    file_name = os.path.splitext(os.path.basename(file_path))[0]
                    for hex_pos, line_nums in unique_lines_by_hex_pos.items():
                        extracted_value = extract_8_characters(file_path, hex_pos, min(line_nums))
                        converted_value = int(extracted_value[::-1], 2)  # Convert
                        commands.append({key: [[hex_pos, 15, 12], [hex_pos, converted_value, 13]]})

                    # Check if key already exists in section_output
                    existing_commands = [cmd for cmd in section_output if cmd.get("id") == key]
                    if existing_commands:
                        existing_commands[0]["cmd"].extend(commands)
                    else:
                        section_output.append({"id": key, "cmd": commands})

                    # Rewrite filtered content to the file
                    with open(file_path, 'w') as file:
                        file.write('\n'.join(filtered_content))

        output[section] = section_output

    output_json = json.dumps(output)
    print(output_json)


# Function definitions for filter_file_content, compare_lines, and extract_8_characters


# Usage
config_file = 'config.ini'
process_files_in_config(config_file)

