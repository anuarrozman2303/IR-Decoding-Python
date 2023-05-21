import configparser

HEXPOS_GROUP_SIZE = 8
HEXPOS_TO_EXCLUDE = [8, 16, 35]

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

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the config file
config.read('config.ini')

# Dictionary to store combined line_nums for each hexpos in each section
combined_line_nums = {}

# Iterate over sections
for section in config.sections():
    print(f"Section: [{section}]")
    file_list = [config.get(section, option) for option in config.options(section)]
    file_count = len(file_list)

    # Compare files
    for i in range(file_count - 1):
        file1_path = file_list[i]
        file2_path = file_list[i + 1]
        diff_lines = compare_files(file1_path, file2_path)
        if diff_lines:
            print(f"Differing lines between {file1_path} and {file2_path}:")
            for line_num, line1, line2 in diff_lines:
                hexpos = (line_num - 1) // HEXPOS_GROUP_SIZE + 1
                if hexpos not in HEXPOS_TO_EXCLUDE:
                    output = f"[{hexpos}:{line_num}] {line1} | {line2}"
                    if section not in combined_line_nums:
                        combined_line_nums[section] = {}
                    if hexpos not in combined_line_nums[section]:
                        combined_line_nums[section][hexpos] = []
                    combined_line_nums[section][hexpos].append(output)

                    # Print 8 characters based on hexpos for each file
                    with open(file1_path, "r") as file1:
                        lines = file1.readlines()
                        start_line = (hexpos - 1) * HEXPOS_GROUP_SIZE
                        end_line = start_line + HEXPOS_GROUP_SIZE
                        hex_sequence = lines[start_line:end_line]
                        characters = ''.join(hex_sequence).replace('\n', '')
                        print(f"Hexpos {hexpos}: {characters}")

                    with open(file2_path, "r") as file2:
                        lines = file2.readlines()
                        start_line = (hexpos - 1) * HEXPOS_GROUP_SIZE
                        end_line = start_line + HEXPOS_GROUP_SIZE
                        hex_sequence = lines[start_line:end_line]
                        characters = ''.join(hex_sequence).replace('\n', '')
                        print(f"Hexpos {hexpos}: {characters}")
            print()

# Print combined line_nums for each hexpos in each section
print("Combined Line Numbers:")
for section, hexpos_dict in combined_line_nums.items():
    print(f"Section: [{section}]")
    for hexpos, line_nums in hexpos_dict.items():
        print(f"Hexpos {hexpos}:")
        for line_num in line_nums:
            print(line_num)
        print()
