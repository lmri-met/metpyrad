# 1. Import the `HidexTDCRProcessor` class
import pandas as pd
from matplotlib import pyplot as plt

from metpyrad import HidexTDCRProcessor

pd.set_option('display.max_columns', None)

# 2. Initialize the Processor: Create an instance of the `HidexTDCRProcessor` class by specifying the radionuclide, year, and month of the measurements:

processor = HidexTDCRProcessor(radionuclide='Lu-177', year=2023, month=11)
print(processor)

# Output:

# Measurements of Lu-177 on November 2023

# 3. Parse Readings: Parse the readings from CSV files provided by the instrument located in a specified folder:

processor.parse_readings(folder_path='hidex_tdcr/test_case/input_files')
print(processor.readings)

# Output:

#    Cycle  Sample  Repetitions  Count rate (cpm)  Counts (reading)  Dead time
# 0      1       1            1             83.97               140      1.000
# 1      1       2            1         252623.23            374237      1.125
# 2      1       1            2             87.57               146      1.000
# 3      1       2            2         251953.09            373593      1.124
# 4      2       1            1             97.77               163      1.000
# 5      2       2            1         223744.10            335987      1.110
# 6      2       1            2             85.17               142      1.000
# 7      2       2            2         223689.40            335843      1.110

# 4. Summarize Readings: Print a summary of the readings and optionally save it to a text file:

processor.summarize_readings()

# Output:

# Measurements of Lu-177 on November 2023
# Summary
# Number of cycles: 2
# Repetitions per cycle: 2
# Time per repetition: 100 s
# Total number of measurements: 4
# Total measurement time: 400 s
# Cycles summary
#    Cycle  Repetitions  Real time (s)                Date
# 0      1            2            100 2023-11-30 08:44:20
# 1      2            2            100 2023-12-01 12:46:16
# Summary saved to output/summary.txt

# 4. Process Measurements: Process the measurements by specifying the type (`background`, `sample`, `net`, or `all`) and the time unit (default is seconds):

processor.process_readings(kind='all', time_unit='s')
print('Background measurements')
print(processor.background)
print('Sample measurements')
print(processor.sample)
print('Net measurements')
print(processor.net)

# Output:

# Background measurements
# Cycle,Sample,Repetitions,Count rate (cpm),Counts (reading),Dead time,Real time (s),End time,Live time (s),Elapsed time,Elapsed time (s),Counts,Counts uncertainty,Counts uncertainty (%)
# 1,1,1,83.97,140,1.0,100,2023-11-30 08:44:20,100.0,0 days 00:00:00,0.0,139.95,11.830046491878212,8.453052155682895
# 1,1,2,87.57,146,1.0,100,2023-11-30 08:51:04,100.0,0 days 00:06:44,404.0,145.95,12.080976781701056,8.277476383488219
# 2,1,1,97.77,163,1.0,100,2023-12-01 12:46:16,100.0,1 days 04:01:56,100916.0,162.95,12.765187033490735,7.833806096036044
# 2,1,2,85.17,142,1.0,100,2023-12-01 12:53:00,100.0,1 days 04:08:40,101320.0,141.95,11.914277149705725,8.393291405217138
# Sample measurements
# Cycle,Sample,Repetitions,Count rate (cpm),Counts (reading),Dead time,Real time (s),End time,Live time (s),Elapsed time,Elapsed time (s),Counts,Counts uncertainty,Counts uncertainty (%)
# 1,2,1,252623.23,374237,1.125,100,2023-11-30 08:47:44,88.88888888888889,0 days 00:00:00,0.0,374256.63703703706,611.7651812885701,0.16346141143464313
# 1,2,2,251953.09,373593,1.124,100,2023-11-30 08:54:28,88.9679715302491,0 days 00:06:44,404.0,373595.9223013048,611.2249359289139,0.1636058906006906
# 2,2,1,223744.1,335987,1.11,100,2023-12-01 12:49:40,90.09009009009009,1 days 04:01:56,100916.0,335952.1021021021,579.6137525129145,0.1725286875379512
# 2,2,2,223689.4,335843,1.11,100,2023-12-01 12:56:24,90.09009009009009,1 days 04:08:40,101320.0,335869.96996996994,579.5428974372561,0.17254978094322423
# Net measurements
# Cycle,Repetitions,Elapsed time,Elapsed time (s),Count rate (cpm),Counts,Counts uncertainty,Counts uncertainty (%)
# 1,1,0 days 00:00:00,0.0,252539.26,374116.68703703705,611.8795527201714,0.16355313032577887
# 1,2,0 days 00:06:44,404.0,251865.52,373449.9723013048,611.3443156694146,0.16370179703110896
# 2,1,1 days 04:01:56,100916.0,223646.33000000002,335789.15210210206,579.7543032199951,0.17265426818901866
# 2,2,1 days 04:08:40,101320.0,223604.22999999998,335728.01996996993,579.6653517073191,0.17265921139354673

# 6. Plot Measurements: Plot the specified type of measurements (`background`, `sample`, or `net`):
processor.plot_measurements(kind='net')
plt.show()

# 7. Export Data: Export the measurements to CSV files and plots to PNG files:

processor.export_measurements_table(kind='net', folder_path='output')
processor.export_measurements_plot(kind='net', folder_path='output')

# Output:

# Net measurements CSV saved to "output" folder.
# Net measurements PNG saved to "output" folder.

# 8. Comprehensive Analysis: Perform a comprehensive analysis, including parsing, processing, summarizing, and exporting the results:

processor.analyze_readings(input_folder='hidex_tdcr/test_case/input_files', time_unit='s', save=True,
                           output_folder='output')

# Output:

# Processing readings from hidex_tdcr/test_case/input_files.
# Found 2 CSV files in folder hidex_tdcr/test_case/input_files
# Measurements summary:
# Measurements of Lu-177 on November 2023
# Summary
# Number of cycles: 2
# Repetitions per cycle: 2
# Time per repetition: 100 s
# Total number of measurements: 4
# Total measurement time: 400 s
# Cycles summary
#    Cycle  Repetitions  Real time (s)                Date
# 0      1            2            100 2023-11-30 08:44:20
# 1      2            2            100 2023-12-01 12:46:16
# Saving measurement files to folder output/Lu-177_2023_11.
# Saving CSV files
# Readings measurements CSV saved to "output/Lu-177_2023_11" folder.
# Background measurements CSV saved to "output/Lu-177_2023_11" folder.
# Sample measurements CSV saved to "output/Lu-177_2023_11" folder.
# Net measurements CSV saved to "output/Lu-177_2023_11" folder.
# All measurements CSV saved to "output/Lu-177_2023_11" folder.
# Summary saved to output/Lu-177_2023_11/summary.txt
# Saving figures
# Backend qtagg is interactive backend. Turning interactive mode on.
# Background measurements PNG saved to "output/Lu-177_2023_11" folder.
# Sample measurements PNG saved to "output/Lu-177_2023_11" folder.
# Net measurements PNG saved to "output/Lu-177_2023_11" folder.
