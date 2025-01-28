from io import StringIO

import pandas as pd

# Data from two Hidex TDCR output csv files Lu-177 2023/11/30 and Lu-177 2023/12/01.
# From both files, the data are from the repetitions 1 and 2.
# CSV formated as the "readings" attribute from "HidexTDCRProcessor" class
_readings_csv = """Cycle,Sample,Repetitions,Count rate (cpm),Counts (reading),Dead time,Real time (s),End time
    1,1,1,83.97,140,1.0,100,2023-11-30 08:44:20
    1,2,1,252623.23,374237,1.125,100,2023-11-30 08:47:44
    1,1,2,87.57,146,1.0,100,2023-11-30 08:51:04
    1,2,2,251953.09,373593,1.124,100,2023-11-30 08:54:28
    2,1,1,97.77,163,1.0,100,2023-12-01 12:46:16
    2,2,1,223744.1,335987,1.11,100,2023-12-01 12:49:40
    2,1,2,85.17,142,1.0,100,2023-12-01 12:53:00
    2,2,2,223689.4,335843,1.11,100,2023-12-01 12:56:24
    """
readings = pd.read_csv(StringIO(_readings_csv))
readings[readings.columns[-1]] = pd.to_datetime(readings[readings.columns[-1]], format='%Y-%m-%d %H:%M:%S')

# Compute background and sample measurements dataframes in the format of the attributes "background" and "sample" from
# "HidexTDCRProcessor" class
_df = readings.copy()
_df['Live time (s)'] = _df['Real time (s)'] / _df['Dead time']
_df['Counts'] = _df['Count rate (cpm)'] * _df['Live time (s)'] / 60
_df['Counts uncertainty'] = _df['Counts'].pow(1 / 2)
_df['Counts uncertainty (%)'] = _df['Counts uncertainty'] / _df['Counts'] * 100
background = _df[_df['Sample'] == _df['Sample'].unique()[0]].reset_index(drop=True)
sample = _df[_df['Sample'] == _df['Sample'].unique()[1]].reset_index(drop=True)

# Compute net quantities dataframes in the format of the attribute "net" from "HidexTDCRProcessor" class
_net_cpm = sample['Count rate (cpm)'] - background['Count rate (cpm)']
_net_counts = sample['Counts'] - background['Counts']
_u_net_counts = (sample['Counts'] + background['Counts']).pow(1 / 2)
_ur_net_counts = _u_net_counts / _net_counts * 100
_initial_time = sample['End time'].min()
_elapsed_time = sample['End time'] - _initial_time
_elapsed_time_seconds = pd.Series([i.total_seconds() for i in _elapsed_time])
_labels = ['Elapsed time', f'Elapsed time (s)', 'Count rate (cpm)', 'Counts', 'Counts uncertainty',
          'Counts uncertainty (%)']
_data = [_elapsed_time, _elapsed_time_seconds, _net_cpm, _net_counts, _u_net_counts, _ur_net_counts]
net = pd.DataFrame(dict(zip(_labels, _data)))

# Concatenate results
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

# Convert attribute DataFrames to CSV strings
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

# Print attribute DataFrames as CSV strings
# These CSV strings can be copied to the corresponding test fixtures for the "HidexTDCRProcessor" class
print(readings_csv)
print(background_csv)
print(sample_csv)
print(net_csv)
print(results_csv)