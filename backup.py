import configparser
import re

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
    file_list = [config.get(section, option) for option in config.options(section)]
    file_count = len(file_list)
    printed_combinations = set()
    if section != "temp":
        print('{"id":"' + section + '","cmd":')
        # Compare files
        for i in range(file_count - 1):
            file1_path = file_list[i]
            file2_path = file_list[i + 1]
            diff_lines = compare_files(file1_path, file2_path)
            if diff_lines:
                for line_num, line1, line2 in diff_lines:
                    hexpos = (line_num - 1) // HEXPOS_GROUP_SIZE + 1
                    if hexpos not in HEXPOS_TO_EXCLUDE:
                        output = f"[{hexpos}:{line_num}] {line1} | {line2}"
                        if section not in combined_line_nums:
                            combined_line_nums[section] = {}
                        if hexpos not in combined_line_nums[section]:
                            combined_line_nums[section][hexpos] = []
                        combined_line_nums[section][hexpos].append(line_num)  # Append only the line_num
                        combination = f"{file1_path}:{hexpos}"
                        if combination not in printed_combinations:
                            with open(file1_path, "r") as file1:
                                lines = file1.readlines()
                                start_line = (hexpos - 1) * HEXPOS_GROUP_SIZE
                                end_line = start_line + HEXPOS_GROUP_SIZE
                                hex_sequence = lines[start_line:end_line]
                                characters = (''.join(hex_sequence).replace('\n', '')[::-1])
                                characters_int = int(characters, 2)  # Convert characters to an integer
                                printed_combinations.add(combination)
                                print('\t{"name":"' + f'{file1_path}"' + f',"inst":[[{hexpos},{characters_int},13]]}}' )

                        combination = f"{file2_path}:{hexpos}"
                        if combination not in printed_combinations:
                            with open(file2_path, "r") as file2:
                                lines = file2.readlines()
                                start_line = (hexpos - 1) * HEXPOS_GROUP_SIZE
                                end_line = start_line + HEXPOS_GROUP_SIZE
                                hex_sequence = lines[start_line:end_line]
                                characters = (''.join(hex_sequence).replace('\n', '')[::-1])
                                characters_int = int(characters, 2)  # Convert characters to an integer
                                printed_combinations.add(combination)
                                print('\t{"name":"' + f'{file2_path}"' + f',"inst":[[{hexpos},{characters_int},13]]}}' )
    else:
        # Compare files
        tfirst = file_list[0]
        tsec = file_list[1]
        tlast = file_list[-1]
        # Extract numeric characters from filenames
        tfirst = float(re.sub(r'\D', '', tfirst))
        tsec = float(re.sub(r'\D', '', tsec))
        tlast = float(re.sub(r'\D', '', tlast))
        # Compare files
        max_characters_int = float('-inf')
        min_characters_int = float('inf')
        disp = tsec - tfirst
        tunit = "C"
        for i in range(file_count - 1):
            file1_path = file_list[i]
            file2_path = file_list[i + 1]
            diff_lines = compare_files(file1_path, file2_path)
            if diff_lines:
                for line_num, line1, line2 in diff_lines:
                    hexpos = (line_num - 1) // HEXPOS_GROUP_SIZE + 1
                    if hexpos not in HEXPOS_TO_EXCLUDE:
                        if section not in combined_line_nums:
                            combined_line_nums[section] = {}
                        if hexpos not in combined_line_nums[section]:   
                            combined_line_nums[section][hexpos] = []
                        combined_line_nums[section][hexpos].append(line_num)  # Append only the line_num
                        combination = f"{file1_path}:{hexpos}"
                        if combination not in printed_combinations:
                            with open(file1_path, "r") as file1:
                                lines = file1.readlines()
                                start_line = (hexpos - 1) * HEXPOS_GROUP_SIZE
                                end_line = start_line + HEXPOS_GROUP_SIZE
                                hex_sequence = lines[start_line:end_line]
                                thex = hexpos
                                characters = (''.join(hex_sequence).replace('\n', '')[::-1])
                                characters_int = int(characters, 2)  # Convert characters to an integer
                                min_characters_int = min(min_characters_int, characters_int)

                        combination = f"{file2_path}:{hexpos}"
                        if combination not in printed_combinations:
                            with open(file2_path, "r") as file2:
                                lines = file2.readlines()
                                start_line = (hexpos - 1) * HEXPOS_GROUP_SIZE
                                end_line = start_line + HEXPOS_GROUP_SIZE
                                hex_sequence = lines[start_line:end_line]
                                characters = (''.join(hex_sequence).replace('\n', '')[::-1])
                                characters_int = int(characters, 2)  # Convert characters to an integer
                                max_characters_int = max(max_characters_int, characters_int)
                                
    # Print combined line_nums for each hexpos in each section
    hexpos_dict = combined_line_nums.get(section, {})
    for hexpos, line_nums in hexpos_dict.items():
        combined_line_nums_set = sorted(set(line_nums))  # Convert line_nums to a set to remove duplicates and sort in ascending order
        combined_line_nums_str = f"[{hexpos}:{', '.join(str(num) for num in combined_line_nums_set)}]"
        # Convert combined_line_nums_set to integers and calculate pos
        pos_values = [num % HEXPOS_GROUP_SIZE for num in combined_line_nums_set]
        if section == "temp":
            continue
        # Process pos_values conditionally for all files
        if all(pos in range(1, 5) for pos in pos_values):
            for file_path in file_list:
                with open(file_path, "r") as file:
                    lines = file.readlines()
                    start_line = (hexpos - 1) * HEXPOS_GROUP_SIZE
                    end_line = start_line + HEXPOS_GROUP_SIZE
                    hex_sequence = lines[start_line:end_line]
                    characters = (''.join(hex_sequence).replace('\n', '')[::-1])
                    characters_int = int(characters, 2)  # Convert characters to an integer
                    print('\t{"name":"' + f'{file_path}"' + f',"inst":[[{hexpos},15,12]]}}' )
        elif any(pos in [5, 6, 7, 0] for pos in pos_values) and not any(pos in [1, 2, 3, 4] for pos in pos_values):
            for file_path in file_list:
                with open(file_path, "r") as file:
                    lines = file.readlines()
                    start_line = (hexpos - 1) * HEXPOS_GROUP_SIZE
                    end_line = start_line + HEXPOS_GROUP_SIZE
                    hex_sequence = lines[start_line:end_line]
                    characters = ''.join(hex_sequence).replace('\n', '')[::-1]
                    characters_int = int(characters, 2)  # Convert characters to an integer
                    print('\t{"name":"' + f'{file_path}"' + f',"inst":[[{hexpos},240,12]]}}')
        else:
            for file_path in file_list:
                with open(file_path, "r") as file:
                    lines = file.readlines()
                    start_line = (hexpos - 1) * HEXPOS_GROUP_SIZE
                    end_line = start_line + HEXPOS_GROUP_SIZE
                    hex_sequence = lines[start_line:end_line]
                    characters = ''.join(hex_sequence).replace('\n', '')[::-1]
                    characters_int = int(characters, 2)  # Convert characters to an integer
                    print('\t{"name":"' + f'{file_path}"' + f',"inst":[[{hexpos},255,12]]}}')
    print()
# Print min_characters_int and max_characters_int side by side
if min_characters_int != float('inf') and max_characters_int != float('-inf'):
    incr = int(max_characters_int / tlast)
    print('\n\n"tCod":[' + f"{incr}," + f"{min_characters_int}," + f"{max_characters_int}],")
    print('"tDis":[' + f"{disp}," + f"{tfirst},{tlast}],")
    print('"tAdd:' f'"{thex}"')
    print('"tUnit:' f'"{tunit}"')