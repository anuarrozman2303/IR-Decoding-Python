import configparser
import os

config = configparser.ConfigParser()
config.read('config.ini')

def process_file(filename, section_name, parent_folder):
    with open(filename, 'r') as f:
        lines = f.readlines()
        # Filter process
        for i in range(len(lines)):
            lines[i] = lines[i].split(':', 1)[-1]
            lines[i] = ''.join([c for c in lines[i] if not c.isalpha( )])
            lines[i] = lines[i].replace(':', '', 1)
        # Remove empty lines & move up the data.
        lines = [line.strip() for line in lines if line.strip()]

        # Sort into groups of 8 consecutive "0" and "1"
        groups = []
        current_group = ''
        for line in lines:
            current_group += line
            if len(current_group) == 8:
                groups.append(current_group)
                current_group = ''
        if current_group:  # In case there's an incomplete group at the end
            groups.append(current_group)

    # Write the groups to a file within the filtered folder for the section
    section_folder = os.path.join(parent_folder, section_name.replace(' ', '_'))
    if not os.path.exists(section_folder):
        os.mkdir(section_folder)
    output_file_name = os.path.splitext(os.path.basename(filename))[0] + '_groups.txt'
    output_file_path = os.path.join(section_folder, output_file_name)
    with open(output_file_path, 'w') as f:
        f.write('\n'.join(groups))
    
    return lines, groups

def compare_filtered_files(filtered_files, output_folder):
    output_file_name = f"diff_{os.path.basename(os.path.dirname(filtered_files[0]))}.txt"
    output_file_path = os.path.join(output_folder, output_file_name)
    
    # Create a dictionary to store the lines based on their hexpos
    hexpos_lines = {}
    for i, file1_path in enumerate(filtered_files):
        for file2_path in filtered_files[i+1:]:
            with open(file1_path, 'r') as f1, open(file2_path, 'r') as f2:
                file1_lines = f1.readlines()
                file2_lines = f2.readlines()
                for line_num, (line1, line2) in enumerate(zip(file1_lines, file2_lines)):
                    if line1 != line2:
                        pos = line_num // 8  # calculate hexpos
                        hexpos = pos + 1
                        if hexpos in [8, 16, 35]:
                            continue  # skip lines with hexpos 8, 16, 35
                        # Add the line to the hexpos_lines dictionary
                        if hexpos not in hexpos_lines:
                            hexpos_lines[hexpos] = set()
                        hexpos_lines[hexpos].add(line_num+1)
    
    # Combine the lines with the same hexpos
    combined_lines = []
    for hexpos in hexpos_lines:
        line_nums = sorted(hexpos_lines[hexpos])
        if len(line_nums) == 1:
            # If there is only one line with the hexpos, add it as is
            combined_lines.append(f"[{hexpos}: {line_nums[0]}]\n")
        else:
            # Otherwise, combine the lines and add them as one line
            combined_lines.append(f"[{hexpos}: {','.join(str(num) for num in line_nums)}]\n")
    
    # Write the combined lines to the output file
    with open(output_file_path, 'w') as f:
        f.writelines(combined_lines)
    print(f"Comparison results saved to {output_file_path}")


parent_folder = "filtered"
if not os.path.exists(parent_folder):
    os.mkdir(parent_folder)

output_folder = "output"
if not os.path.exists(output_folder):
    os.mkdir(output_folder)

for section in config.sections():
    section_name = section.replace(' ', '_')
    section_folder = os.path.join(parent_folder, section_name)
    if not os.path.exists(section_folder):
        os.mkdir(section_folder)
    output_section_folder = os.path.join(output_folder, section_name)
    if not os.path.exists(output_section_folder):
        os.mkdir(output_section_folder)
    filtered_files = []
    for key in config[section]:
        file_path = config[section][key]
        lines, groups = process_file(file_path, section_name, parent_folder)
        filtered_file_path = os.path.join(section_folder, os.path.basename(file_path))
        with open(filtered_file_path, 'w') as f:
            f.write('\n'.join(lines))
        filtered_files.append(filtered_file_path)
    compare_filtered_files(filtered_files, output_section_folder)


