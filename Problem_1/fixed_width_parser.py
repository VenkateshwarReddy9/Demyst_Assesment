import json
import csv

def load_spec(spec_file):
    """
    Load the specifications from the JSON file.
    """
    with open(spec_file, 'r', encoding='utf-8') as file:
        spec = json.load(file)
        
        column_names = spec['ColumnNames']
        offsets = list(map(int, spec['Offsets']))
        fixed_width_encoding = spec.get('FixedWidthEncoding', 'utf-8')
        delimited_encoding = spec.get('DelimitedEncoding', 'utf-8')
        include_header = spec.get('IncludeHeader', 'True') == "True"
        
        return {
            "column_names": column_names,
            "offsets": offsets,
            "fixed_width_encoding": fixed_width_encoding,
            "delimited_encoding": delimited_encoding,
            "include_header": include_header
        }

def generate_fixed_width_input_file(spec, output_file):
    
    #Generates a fixed-width input file based on the provided specification.
    
    offsets = spec['offsets']
    fixed_width_encoding = spec['fixed_width_encoding']

    #  example data
    example_data = [
        ["John", "Doe", "35", "M", "123 Main St.", "NY", "10001", "USA", "john.doe@email.com", "1234567890"],
        ["Jane", "Smith", "28", "F", "456 Elm St.", "CA", "90210", "USA", "jane.smith@email.com", "9876543210"]
    ]

    def format_fixed_width(row, offsets):
        """
        Format a single row into fixed-width format using offsets.
        """
        fixed_width_row = ''
        for value, width in zip(row, offsets):
            fixed_width_row += value.ljust(width)[:width]  # Left-justify and trim/pad to fit width
        return fixed_width_row

    with open(output_file, 'w', encoding=fixed_width_encoding) as outfile:
        
        # Write example data rows
        for row in example_data:
            outfile.write(format_fixed_width(row, offsets) + '\n')

def parse_fixed_width_to_csv(spec, input_file, output_file):
    
    #Parse a fixed-width file and write its content to a delimited (CSV) file.
    
    offsets = spec['offsets']
    column_names = spec['column_names']
    fixed_width_encoding = spec['fixed_width_encoding']
    delimited_encoding = spec['delimited_encoding']
    include_header = spec['include_header']

    # Compute field start and end positions
    start_pos = 0
    positions = []
    for length in offsets:
        end_pos = start_pos + length
        positions.append((start_pos, end_pos))
        start_pos = end_pos

    # Process the fixed-width file and write to CSV
    with open(input_file, 'r', encoding=fixed_width_encoding) as infile, \
         open(output_file, 'w', encoding=delimited_encoding, newline='') as outfile:
        writer = csv.writer(outfile)
        
        if include_header:
            writer.writerow(column_names)
        
        for line in infile:
            row = [line[start:end].strip() for start, end in positions]
            writer.writerow(row)

# Main Execution
if __name__ == "__main__":
    # Load specifications
    spec = load_spec("specs.json")

    # Generate a fixed-width input file
    generate_fixed_width_input_file(
        spec=spec,
        output_file="input_fixed_width.txt"
    )

    # Parse the fixed-width file and generate a CSV
    parse_fixed_width_to_csv(
        spec=spec,
        input_file="input_fixed_width.txt",
        output_file="output.csv"
    )
