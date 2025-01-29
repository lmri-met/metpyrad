# What a user may want to do with the readings of the Hidex TDCR?
# 1. Simply extract some information of the readings.
# 2. Get a summary of the measurements.
# 3. Compute some quantities for the background and sample measurements.
# 4. Compute some net quantities from the background and sample measurements.
# 5. Get a compilation of all of these results.
# 6. Make some plots of some of these results.
# 7. Save any of these results to csv or images.
# 8. Make a complete analysis that includes all the previous steps.
import os

from matplotlib import pyplot as plt

from metpyrad.hidex_tdcr import HidexTDCRProcessor

processor = HidexTDCRProcessor(radionuclide='Lu-177', year=2023, month=11)
# TODO: Check code coverage (maybe organise test in numeric results, IO and exceptions)

# 1. Simply extract some information of the readings.
processor.get_readings(folder_path='test_case/input_files')
print(processor.readings)

# 3. Compute some quantities for the background measurements.
processor.get_background_measurements()
print(processor.background)

# 3. Compute some quantities for the sample measurements.
processor.get_sample_measurements()
print(processor.sample)
# TODO: Maybe the elapsed time may be included in the background and measurements tables

# 4. Compute some net quantities from the background and sample measurements.
processor.get_net_measurements(time_unit='s')
print(processor.net)
# TODO: Maybe the cycle, repetition and end time elapsed time should be included in the net quantities table

# 5. Get a compilation of all of these results.
results = processor.compile_measurements()
print(results)
# TODO: Minimize columns in output table

# 2. Get a summary of the measurements (export to txt file availabe).
processor.summarize_readings()

# # 6. Make some plots of some of these results.
# # Plot of the background measurements
# processor.plot_measurements(kind='background')
# plt.show()
# # Plot of the sample measurements
# processor.plot_measurements(kind='sample')
# plt.show()
# # Plot of the net quantities
# processor.plot_measurements(kind='net')
# plt.show()

# # 7. Save any of these results to csv or images
# # Create an output folder
# os.makedirs('output', exist_ok=True)
# # Save results to csv files.
# # Readings table
# processor.export_measurements_table(kind='readings', folder_path='output')
# # Background measurements table
# processor.export_measurements_table(kind='background', folder_path='output')
# # Sample measurements table
# processor.export_measurements_table(kind='sample', folder_path='output')
# # Net quantities measurements table
# processor.export_measurements_table(kind='net', folder_path='output')
# # Table with background, sample and net measurements
# processor.export_measurements_table(kind='all', folder_path='output')
# # Save plots to images
# # Plot of the background measurements
# processor.export_measurements_plot(kind='background', folder_path='output')
# # Plot of the sample measurements
# processor.export_measurements_plot(kind='sample', folder_path='output')
# # Plot of the net quantities
# processor.export_measurements_plot(kind='net', folder_path='output')

# # 8. Make a complete analysis that includes all the previous steps.
# results2 = processor.process_readings(folder_path='test_case/input_files', time_unit='s', save=True)
# # TODO: The user may want to choose where the output folder is saved
