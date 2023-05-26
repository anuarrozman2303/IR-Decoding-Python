def replace_string_in_file(file_path, search_strings, replacement_strings):
    with open(file_path, 'r') as file:
        content = file.read()

    for i in range(len(search_strings)):
        search_string = search_strings[i]
        replacement_string = replacement_strings[i]
        content = content.replace(search_string, replacement_string)

    with open(file_path, 'w') as file:
        file.write(content)

# Specify the file path, search strings, and replacement strings
file_path = 'output.json'
search_strings = ['{"power":', '"mode":', '"fan":', '"vlourve":', '"hlourve":', '"misc1":', '"misc2":', ']}]}, "tCod":']
replacement_strings = ['', '', '', '', '', '', '', ']}]}], "tCod":']

# Call the function to replace the strings in the file
replace_string_in_file(file_path, search_strings, replacement_strings)
