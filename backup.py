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
            lines[i] = ''.join([c for c in lines[i] if not c.isalpha()])
            lines[i] = lines[i].replace(':', '', 1)
        # Remove empty lines & move up the data.
        lines = [line.strip() for line in lines if line.strip()]
    return lines

def print_consecutive_lines(section_name, filtered_files):
    for file_path in filtered_files:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            hexpos_count = 0
            consecutive_lines = []
            for line_num, line in enumerate(lines):
                hexpos_count += 1
                if hexpos_count == 8:
                    hexpos_count = 0
                    consecutive_lines.append(line.strip())
                    if len(consecutive_lines) == 8:
                        print(f"Section: {section_name}")
                        print(' '.join(consecutive_lines))
                        consecutive_lines = []
                else:
                    consecutive_lines.append(line.strip())
            if consecutive_lines:
                print(f"Section: {key}")
                print(' '.join(consecutive_lines))

parent_folder = "filtered"
if not os.path.exists(parent_folder):
    os.mkdir(parent_folder)

for section in config.sections():
    section_name = section.replace(' ', '_')
    section_folder = os.path.join(parent_folder, section_name)
    if not os.path.exists(section_folder):
        os.mkdir(section_folder)
    filtered_files = []
    for key in config[section]:
        file_path = config[section][key]
        lines = process_file(file_path, section_name, parent_folder)
        filtered_file_path = os.path.join(section_folder, os.path.basename(file_path))
        with open(filtered_file_path, 'w') as f:
            f.write('\n'.join(lines))
        filtered_files.append(filtered_file_path)
    print_consecutive_lines(section, filtered_files)
    print()
