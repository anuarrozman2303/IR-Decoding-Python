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
    print('{"id":"' + section + '","cmd":')

    file_list = [config.get(section, option) for option in config.options(section)]
    file_count = len(file_list)

    for i in range(file_count - 1):
        file1_path = file_list[i]
        file2_path = file_list[i + 1]

        # ... (existing code remains the same)

        for hexpos, line_nums in hexpos_dict.items():
            # ... (existing code remains the same)

            # Convert combined_line_nums_set to integers and calculate pos
            pos_values = [num % HEXPOS_GROUP_SIZE for num in combined_line_nums_set]
            print("pos:", pos_values)

            # Process pos_values conditionally
            if all(pos in range(1, 5) for pos in pos_values):
                print('\t{"name:"' f'"{file1_path}",' + "inst:" f"[[{hexpos},15,12]]" )

            # ... (existing code remains the same)

    print()
