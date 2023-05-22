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
    # Remaining code for file comparison...

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the config file
config.read('config.ini')

# List to store filtered content of each file
filtered_content_list = []

# Iterate over sections
for section in config.sections():
    file_list = [config.get(section, option) for option in config.options(section)]
    file_count = len(file_list)
    printed_combinations = set()
    
    if section != "temp":
        # Filter files and store the filtered content
        filtered_content = [filter_file_content(file_path) for file_path in file_list]
        filtered_content_list.extend(filtered_content)
        
        # Overwrite the files with the filtered content
        for file_path, filtered_content in zip(file_list, filtered_content):
            with open(file_path, 'w') as f:
                f.write('\n'.join(filtered_content))
                
        # Perform comparison and other output
        for i in range(file_count - 1):
            file1_path = file_list[i]
            file2_path = file_list[i + 1]
            diff_lines = compare_files(file1_path, file2_path)
            # Remaining code for comparison and output...
    else:
        # Remaining code for file comparison and printing...
        
# Print combined line_nums for each hexpos in each section
# Remaining code for printing combined line_nums...

# Print min_characters_int and max_characters_int side by side
# Remaining code for printing min_characters_int and max_characters_int...
