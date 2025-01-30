# 1. Import the `HidexTDCRProcessor` class
import pandas as pd
from matplotlib import pyplot as plt

from metpyrad import HidexTDCRProcessor

pd.set_option('display.max_columns', None)

# 2. Initialize the Processor: Create an instance of the `HidexTDCRProcessor` class by specifying the radionuclide, year, and month of the measurements:
processor = HidexTDCRProcessor(radionuclide='Lu-177', year=2023, month=11)
print(processor)

# 3. Parse Readings: Parse the readings from CSV files provided by the instrument located in a specified folder:
processor.parse_readings(folder_path='hidex_tdcr/test_case/input_files')
print(processor.readings)

# 4. Summarize Readings: Print a summary of the readings and optionally save it to a text file:
processor.summarize_readings()

# 5. Process Measurements: Process the measurements by specifying the type (`background`, `sample`, `net`, or `all`) and the time unit (default is seconds):
processor.process_readings(kind='all', time_unit='s')
print('Background measurements')
print(processor.background)
print('Sample measurements')
print(processor.sample)
print('Net measurements')
print(processor.net)

# 6. Plot Measurements: Plot the specified type of measurements (`background`, `sample`, or `net`):
processor.plot_measurements(kind='sample')
processor.plot_measurements(kind='net')
plt.show()

# 7. Export Data: Export the measurements to CSV files and plots to PNG files:
processor.export_measurements_table(kind='net', folder_path='output')
processor.export_measurements_plot(kind='net', folder_path='output')

# 8. Comprehensive Analysis: Perform a comprehensive analysis, including parsing, processing, summarizing, and exporting the results:

processor.analyze_readings(input_folder='hidex_tdcr/test_case/input_files', time_unit='s', save=True,
                           output_folder='output')
