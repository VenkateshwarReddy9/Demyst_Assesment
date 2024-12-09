import unittest
import os
from fixed_width_parser import parse_fixed_width_to_csv, generate_fixed_width_input_file, load_spec

class TestParser(unittest.TestCase):
    def setUp(self):
        
        #Setup for the tests: create a mock input file.
        
        self.spec = {
            "column_names": ["f1", "f2", "f3"],
            "offsets": [5, 10, 15],
            "fixed_width_encoding": "utf-8",
            "delimited_encoding": "utf-8",
            "include_header": True
        }
        self.input_file = "test_fixed_width.txt"
        self.output_file = "test_output.csv"

        # Generate a mock input fixed-width file
        example_data = [
            ["John", "Doe", "12345"],
            ["Jane", "Smith", "67890"]
        ]

        with open(self.input_file, "w", encoding=self.spec["fixed_width_encoding"]) as file:
            for row in example_data:
                line = "".join(value.ljust(width) for value, width in zip(row, self.spec["offsets"]))
                file.write(line + "\n")

    def tearDown(self):
        
        #Cleanup after tests: remove test files.
        
        if os.path.exists(self.input_file):
            os.remove(self.input_file)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_parse_fixed_width(self):
        
        #Test parsing a fixed-width file into a CSV.
        
        parse_fixed_width_to_csv(self.spec, self.input_file, self.output_file)

        # Validate the CSV content
        with open(self.output_file, "r", encoding=self.spec["delimited_encoding"]) as file:
            lines = file.readlines()

        self.assertEqual(lines[0].strip(), "f1,f2,f3")  # Header
        self.assertEqual(lines[1].strip(), "John,Doe,12345")  # First row
        self.assertEqual(lines[2].strip(), "Jane,Smith,67890")  # Second row

if __name__ == "__main__":
    unittest.main()
