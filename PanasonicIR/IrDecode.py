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


def rewrite_file(filename, lines):
    with open(filename, 'w') as f:
        f.write('\n'.join(lines))


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


def process_files_in_config(config_file):
    with open('PanasonicIR/output.json', 'w') as f:
        config = configparser.ConfigParser()
        config.read(config_file)

        excluded_hex_pos = [8, 16, 35]  # List of excluded hex_pos values

        output = {}
        output["code"] = [17, 218, 39, 0, 197, 16, 0, 0, 17, 218, 39, 0, 66, 170, 35, 0, 17, 218, 39, 0, 0, 40, 36, 0, 0, 0, 0, 6, 96, 0, 0, 197, 0, 8, 0]
        output["cmdGr"] = []

        for section in config.sections():
            filtered_files = {}

            # Filter files
            for key in config[section]:
                file_path = config[section][key]
                try:
                    filtered_content = filter_file_content(file_path)
                    filtered_files[key] = (filtered_content, file_path)
                except FileNotFoundError:
                    print(f"File not found: {file_path}")

            # Rewrite filtered content to the files
            for key, (filtered_content, file_path) in filtered_files.items():
                rewrite_file(file_path, filtered_content)

            # Compare filtered key-value pairs
            keys = list(filtered_files.keys())
            diff_info_by_section = {}  # Dictionary to store diff_info by section
            for i in range(len(keys) - 1):
                key1 = keys[i]
                value1, file1 = filtered_files[key1]
                for j in range(i + 1, len(keys)):
                    key2 = keys[j]
                    value2, file2 = filtered_files[key2]
                    diff_info = compare_lines(value1, value2, excluded_hex_pos)
                    if diff_info:
                        diff_info_by_section.setdefault(section, []).extend(diff_info)

            # Combine unique line numbers by hex_pos for each section
            unique_lines_by_hex_pos = {}
            for hex_pos, line_num in diff_info_by_section.get(section, []):
                unique_lines_by_hex_pos.setdefault(hex_pos, set()).add(line_num)
            if section != "temp":
                # Append output for the same file_name
                if unique_lines_by_hex_pos:
                    for hex_pos, line_nums in unique_lines_by_hex_pos.items():
                        for key, (filtered_content, file_path) in filtered_files.items():
                            if key in config[section]:
                                file_name = os.path.splitext(os.path.basename(file_path))[0]
                                extracted_value = extract_8_characters(file_path, hex_pos, min(line_nums))
                                pos = [num % 8 for num in line_nums]
                                setToZero = []
                                if all(p in range(1, 5) for p in pos):
                                    setToZero = 15
                                    extracted_value = "".join([val if i + 1 not in [5, 6, 7, 8] else "0" for i, val in enumerate(extracted_value)])
                                elif any(p in [5, 6, 7, 0] for p in pos) and not any(p in [1, 2, 3, 4] for p in pos):
                                    setToZero = 240
                                    extracted_value = "".join([val if i + 1 not in [0, 1, 2, 3] else "0" for i, val in enumerate(extracted_value)])
                                else:
                                    setToZero = 255
                                reversed_value = extracted_value[::-1]
                                converted_value = int(reversed_value, 2)  # Convert
                                section_data = {"id": section, "cmd": []}
                                existing_sections = [item["id"] for item in output["cmdGr"]]
                                if section not in existing_sections:
                                    output["cmdGr"].append(section_data)
                                for item in output["cmdGr"]:
                                    if item["id"] == section:
                                        file_inst = item["cmd"]
                                        existing_file_names = [inst["name"] for inst in file_inst]
                                        if file_name not in existing_file_names:
                                            file_inst.append({"name": file_name, "inst": []})
                                        for inst in file_inst:
                                            if inst["name"] == file_name:
                                                # Exclude command with hex_pos = 23 for section = mode and file name = Cool
                                                if hex_pos == 23 and section == "mode" and file_name == "Cool":
                                                    continue
                                                inst["inst"].append([hex_pos, setToZero, 12])
                                                inst["inst"].append([hex_pos, converted_value, 13])
                                                break
                    # Rewrite filtered content to the files
                    for key, (filtered_content, file_path) in filtered_files.items():
                        rewrite_file(file_path, filtered_content)
            else:  ##temp
                if unique_lines_by_hex_pos:
                    first_comparison_values = []  # List to store values from the first comparison
                    last_comparison_values = []  # List to store values from the last comparison

                    for hex_pos, line_nums in unique_lines_by_hex_pos.items():
                        for key, (filtered_content, file_path) in filtered_files.items():
                            if key in config[section]:
                                file_name = os.path.splitext(os.path.basename(file_path))[0]
                                extracted_value = extract_8_characters(file_path, hex_pos, min(line_nums))
                                converted_value = int((extracted_value[::-1]), 2)

                                if hex_pos == min(unique_lines_by_hex_pos.keys()):  # First comparison
                                    first_comparison_values.append(converted_value)
                                if hex_pos == max(unique_lines_by_hex_pos.keys()):  # Last comparison
                                    last_comparison_values.append(converted_value)

                    mintemp = min(first_comparison_values) if first_comparison_values else None
                    maxtemp = max(last_comparison_values) if last_comparison_values else None
                    file_names = [re.sub(r'\D', '', os.path.splitext(os.path.basename(file_path))[0]) for key, (_, file_path) in filtered_files.items() if key in config[section]]
                    tfirst = float(file_names[0]) if file_names else None
                    tsec = float(file_names[1]) if len(file_names) >= 2 else None
                    tlast = float(file_names[-1]) if file_names else None
                    tinc = tsec - tfirst
                    tdis = int(maxtemp / tlast)
                    tunit = "C"
                    thex = hex_pos

        # Append values to output JSON
        output.setdefault("tCod", []).extend([tdis, mintemp, maxtemp])
        output.setdefault("tDis", []).extend([tinc, tfirst, tlast])
        output["tAdd"] = thex
        output["tUnit"] = tunit
        output["cSum"] = chsum_address
        output["cInf"] = values
        output["cPre"] = pre
        output["cConf"] = conf
        output["id"] = dev

        output_json = json.dumps(output)
        f.write(output_json)

# Provide the path to your config file here
config_file_path = 'PanasonicIR\config.ini'
process_files_in_config(config_file_path)

