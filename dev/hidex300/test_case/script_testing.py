import os
from calendar import month_name
from io import StringIO

import pandas as pd

# Data from four Hidex 300 output csv files for Lu-177: 2023/11/30, 2023/12/06, 2023/12/12 and 2023/12/22.
# From all files, the data are from the repetitions 1 and 2.

# Part 0: Readings summary
# ------------------------

_radionuclide, _month, _year = 'Lu-177', 11, 2023
_cycles, _cycle_repetitions, _repetition_time, _total_measurements, _measurement_time = 4, 2, 100, 8, 800
msg = (f'Measurements of {_radionuclide} on {month_name[_month]} {_year}\n'
       f'Summary\n'
       f'Number of cycles: {_cycles}\n'
       f'Repetitions per cycle: {_cycle_repetitions}\n'
       f'Time per repetition: {_repetition_time} s\n'
       f'Total number of measurements: {_total_measurements}\n'
       f'Total measurement time: {_measurement_time} s\n'
       f'Cycles summary\n'
       f'   Cycle  Repetitions  Real time (s)                Date\n'
       f'0      1            2            100 2023-11-30 08:44:20\n'
       f'1      2            2            100 2023-12-06 10:23:19\n'
       f'2      3            2            100 2023-12-12 08:41:22\n'
       f'3      4            2            100 2023-12-22 08:47:48')

# Part 1: Compute readings dataframe in the format of the attributes "readings"from Hidex300 class
# ------------------------------------------------------------------------------------------------

# Foder with test case input files
folder_path = 'input_files'
# Rows to extract from the CSV files
_ROWS_TO_EXTRACT = ['Samp.', 'Repe.', 'CPM', 'Counts', 'DTime', 'Time', 'EndTime']
# Format for parsing date and time strings from the CSV files
_DATE_TIME_FORMAT = '%d/%m/%Y %H:%M:%S'
# String that indicates the start of a data block in the CSV files
_BLOCK_STARTER = 'Sample start'
# Number of initial lines to skip from the CSV files
_ID_LINES = 4
# Delimiter used in the CSV files
_DELIMITER = ';'
# List to store csv files with their full paths
_input_files = []
# Iterate over all the files in the given folder
for _file_name in os.listdir(folder_path):
    # Check if the file has a .csv extension
    if _file_name.endswith('.csv'):
        # Append the absolute path of the file to the list
        _input_files.append(os.path.abspath(os.path.join(folder_path, _file_name)))
# Initialize a list to store extracted data
_extracted_data = []
# Iterate over each CSV file
for _file_number, _input_file in enumerate(_input_files, start=1):
    # Open the current CSV file
    with open(_input_file, 'r') as _file:
        # Read all lines from the file
        _lines = _file.readlines()
        # Initialize a dictionary to store the current data block
        _current_block = {}
        # Iterate over the lines, skipping the initial ID lines
        for _line in _lines[_ID_LINES:]:
            # Check if the line indicates the start of a new data block
            if _line.strip() == _BLOCK_STARTER:
                # If there is an existing data block, append it to the extracted data
                if _current_block:
                    _extracted_data.append(_current_block)
                # Initialize a new data block with the file number
                _current_block = {'file': _file_number}
            else:
                # Extract relevant rows from the line
                for _row in _ROWS_TO_EXTRACT:
                    if _line.startswith(_row):
                        _current_block[_row] = _line.split(_DELIMITER)[1].strip()
        # Append the last data block if it exists
        if _current_block:
            _extracted_data.append(_current_block)
# Convert the extracted data to a DataFrame
_df = pd.DataFrame(_extracted_data, columns=_ROWS_TO_EXTRACT + ['file'])
# Convert relevant columns to numeric values
for _col in _df.columns[:-2]:
    _df[_col] = pd.to_numeric(_df[_col])
# Convert the date and time column to datetime format
_df[_df.columns[-2]] = pd.to_datetime(_df[_df.columns[-2]], format=_DATE_TIME_FORMAT)
# Sort the DataFrame by the end time
_df = _df.sort_values(by='EndTime')
_df = _df.reset_index(drop=True)
# Check if repetitions per cycle are consistent for all measurements
_value_counts = _df['file'].value_counts()
# Reassign values to files according to chronological order
_df['file'] = [i for i in range(1, _df['file'].unique().size + 1) for _ in range(_value_counts.unique()[0])]
# Move the last column to be the first
_cols = _df.columns.tolist()
_cols = [_cols[-1]] + _cols[:-1]
_df = _df[_cols]
# Rename columns for clarity
_old_names = ['file', 'Samp.', 'Repe.', 'CPM', 'Counts', 'DTime', 'Time', 'EndTime']
_new_names = ['Cycle', 'Sample', 'Repetition', 'Count rate (cpm)', 'Counts (reading)', 'Dead time',
             'Real time (s)', 'End time']
_df = _df.rename(columns=dict(zip(_old_names, _new_names)))
readings = _df

# Part 2: Compute background and sample measurements dataframes in the format of
# the attributes "background" and "sample" from Hidex300 class
# ------------------------------------------------------------------------------------------------

_df = readings.copy()
background = _df[_df['Sample'] == _df['Sample'].unique()[0]].reset_index(drop=True)
background['Live time (s)'] = background['Real time (s)'] / background['Dead time']
_initial_time = background['End time'].min()
background['Elapsed time'] = background['End time'] - _initial_time
background[f'Elapsed time (s)'] = pd.Series([i.total_seconds() for i in background['Elapsed time']])
background['Counts'] = background['Count rate (cpm)'] * background['Live time (s)'] / 60
background['Counts uncertainty'] = background['Counts'].pow(1 / 2)
background['Counts uncertainty (%)'] = background['Counts uncertainty'] / background['Counts'] * 100

_df = readings.copy()
sample = _df[_df['Sample'] == _df['Sample'].unique()[1]].reset_index(drop=True)
sample['Live time (s)'] = sample['Real time (s)'] / sample['Dead time']
_initial_time = sample['End time'].min()
sample['Elapsed time'] = sample['End time'] - _initial_time
sample[f'Elapsed time (s)'] = pd.Series([i.total_seconds() for i in sample['Elapsed time']])
sample['Counts'] = sample['Count rate (cpm)'] * sample['Live time (s)'] / 60
sample['Counts uncertainty'] = sample['Counts'].pow(1 / 2)
sample['Counts uncertainty (%)'] = sample['Counts uncertainty'] / sample['Counts'] * 100

# Part 3: Compute net quantities dataframes in the format of the attribute "net" from Hidex300 class
# --------------------------------------------------------------------------------------------------
_cycle = sample['Cycle']
_repetition = sample['Repetition']
_net_cpm = sample['Count rate (cpm)'] - background['Count rate (cpm)']
_net_counts = sample['Counts'] - background['Counts']
_u_net_counts = (sample['Counts'] + background['Counts']).pow(1 / 2)
_ur_net_counts = _u_net_counts / _net_counts * 100
_initial_time = sample['End time'].min()
_elapsed_time = sample['End time'] - _initial_time
_elapsed_time_seconds = pd.Series([i.total_seconds() for i in _elapsed_time])
_labels = ['Cycle', 'Repetition', 'Elapsed time', f'Elapsed time (s)', 'Count rate (cpm)', 'Counts',
           'Counts uncertainty', 'Counts uncertainty (%)']
_data = [_cycle, _repetition, _elapsed_time, _elapsed_time_seconds, _net_cpm, _net_counts, _u_net_counts, _ur_net_counts]
net = pd.DataFrame(dict(zip(_labels, _data)))

# Part 4: Concatenate background, sample and net dataframes
# ---------------------------------------------------------

# Sample DataFrames
_df1 = background.copy()
_df2 = sample.copy()
_df3 = net.copy()
# Creating multi-level headers
_header1 = pd.MultiIndex.from_product([['Background'], _df1.columns])
_header2 = pd.MultiIndex.from_product([['Sample'], _df2.columns])
_header3 = pd.MultiIndex.from_product([['Net'], _df3.columns])
# Assigning the multi-level headers to the DataFrames
_df1.columns = _header1
_df2.columns = _header2
_df3.columns = _header3
# Concatenating the DataFrames
results = pd.concat([_df1, _df2, _df3], axis=1)

# Part 5: Convert attribute DataFrames to CSV strings
# ---------------------------------------------------

# Readings
_csv_buffer = StringIO()
readings.to_csv(_csv_buffer, index=False)
readings_csv = _csv_buffer.getvalue()
# Background
_csv_buffer = StringIO()
background.to_csv(_csv_buffer, index=False)
background_csv = _csv_buffer.getvalue()
# Sample
_csv_buffer = StringIO()
sample.to_csv(_csv_buffer, index=False)
sample_csv = _csv_buffer.getvalue()
# Net
_csv_buffer = StringIO()
net.to_csv(_csv_buffer, index=False)
net_csv = _csv_buffer.getvalue()
# Results
_csv_buffer = StringIO()
results.to_csv(_csv_buffer, index=False)
results_csv = _csv_buffer.getvalue()

# Part 6: Print results for tests
# -------------------------------

# Print attribute DataFrames as CSV strings
# These CSV strings can be copied to the corresponding test fixtures for the "HidexTDCR" class
print(str(msg))
print(readings_csv)
print(background_csv)
print(sample_csv)
print(net_csv)
print(results_csv)