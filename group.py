def convert_to_hex(binary_sequence):
    binary_string = ''.join(binary_sequence).replace('\n', '')
    decimal_value = int(binary_string, 2)
    hex_value = hex(decimal_value)[2:]  # Remove the '0x' prefix
    return hex_value


file_path = "on.txt"  # Replace with the actual file path

with open(file_path, "r") as file:
    lines = file.readlines()

num_lines = len(lines)
num_hex_positions = num_lines // 8

for pos in range(num_hex_positions):
    start_line = pos * 8
    end_line = start_line + 8
    hex_sequence = lines[start_line:end_line]
    characters = ''.join(hex_sequence).replace('\n', '')
    print(f"hexpos {pos+1} : {characters}")
