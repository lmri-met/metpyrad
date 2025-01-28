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
# TODO: Maybe add methods to export tables as csv and plots as images.

# 1. Simply extract some information of the readings.
processor.parse_csv_files(folder_path='test_case/input_files')
print(processor.readings)
# TODO: Naming: parse_readings instead of parse_csv_files?

# 2. Get a summary of the measurements.
processor.get_statistics()
print(processor.summary)
# TODO: Naming: get_measurements_statistics instead of get_statistics?
# TODO: The user may not only want to see the table, but the complete summary that is printed when __str__ is called

# 3. Compute some quantities for the background and sample measurements.
processor.get_background_sample_df()
print(processor.background)
print(processor.sample)
# TODO: Naming: get_background_measurements and get_sample_measurements instead of get_background_sample_df?
# TODO: Maybe the elapsed time may be included in the background and measurements tables

# 4. Compute some net quantities from the background and sample measurements.
processor.get_net_quantities_df(time_unit='s')
print(processor.net)
# TODO: Naming: get_net_measurements instead of get_net_quantities_df?
# TODO: Maybe the cycle, repetition and end time elapsed time should be included in the net quantities table

# 5. Get a compilation of all of these results.
results = processor.concatenate_results()
print(results)
# TODO: Minimize columns in output table

# 6. Make some plots of some of these results.
# Plot of the background measurements
processor.plot_readings(sample='background')
plt.show()
# Plot of the sample measurements
processor.plot_readings(sample='sample')
plt.show()
# Plot of the net quantities
processor.plot_net_quantities()
plt.show()

# 7. Save any of these results to csv
# Create an output folder
os.makedirs('output', exist_ok=True)
# Save results to csv files.
# Readings table
processor.readings.to_csv('output/readings.csv', index=False)
# Measurements summary table
processor.summary.to_csv('output/summary.csv', index=False)
# Background measurements table
processor.background.to_csv('output/background.csv', index=False)
# Sample measurements table
processor.sample.to_csv('output/sample.csv', index=False)
# Net quantities measurements table
processor.net.to_csv('output/net.csv', index=False)
# Table with background, sample and net measurements
results.to_csv('output/results.csv', index=False)
# Save plots to images
# Plot of the background measurements
processor.plot_readings(sample='background')
plt.savefig('output/background.png')
# Plot of the sample measurements
processor.plot_readings(sample='sample')
plt.savefig('output/sample.png')
# Plot of the net quantities
processor.plot_net_quantities()
plt.savefig('output/net.png')

# 8. Make a complete analysis that includes all the previous steps.
results2 = processor.process_readings(folder_path='test_case/input_files', time_unit='s', save=True)
# TODO: The user may want to choose where the output folder is saved