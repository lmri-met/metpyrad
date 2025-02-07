# Getting started
import pandas as pd

from metpyrad import HidexTDCR

pd.set_option('display.max_columns', None)

# Initialize the processor
processor = HidexTDCR(radionuclide='Lu-177', year=2023, month=11)
print(processor)

# Path to the folder containing the CSV files
folder_path = '../hidex_tdcr/test_case/input_files'

# Parse the readings
processor.parse_readings(folder_path)

# Inspect the parsed readings
print(processor.readings)

# Print the summary of the measurements
print(processor)
