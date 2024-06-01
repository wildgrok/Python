import csv

# Define file paths
workfolder = 'C:/Users/admin/OneDrive/Documents/python/'
data_file_path =  workfolder + 'DataFile.txt'
lookup_file_path = workfolder + 'LookupFile.txt'
output_file_path = workfolder + 'OutputFile.txt'

# Read the lookup file and create a dictionary
lookup_table = {}
with open(lookup_file_path, mode='r') as lookup_file:
    reader = csv.reader(lookup_file)
    for row in reader:
        key, value = row
        lookup_table[key] = value

# Read the data file and process each row
output_lines = []
with open(data_file_path, mode='r') as data_file:
    reader = csv.reader(data_file)
    headers = next(reader)  # Read the header row
    headers.append('LookupValue')
    output_lines.append(headers)  # Add headers to the output

    for row in reader:
        id_, name, key = row
        lookup_value = lookup_table.get(key, 'Not Found')
        output_lines.append([id_, name, key, lookup_value])

# Write the output to a new file
with open(output_file_path, mode='w', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerows(output_lines)

print(f"Output written to {output_file_path}")
