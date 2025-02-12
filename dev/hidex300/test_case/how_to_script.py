import pandas as pd
from matplotlib import pyplot as plt

from metpyrad import Hidex300

pd.set_option('display.max_columns', None)
input_folder = 'input_files'
output_folder = '../../../output'

processor = Hidex300(radionuclide='Lu-177', year=2023, month=11)
processor.parse_readings(folder_path=input_folder)
# print(processor.readings)

# processor.process_readings(kind='background')
# print(processor.background)
# processor.process_readings(kind='sample')
# print(processor.sample)
# processor.process_readings(kind='net')
# print(processor.net)
processor.process_readings(kind='all')

# processor.summarize_readings()
# processor.summarize_readings(save=True, folder_path=output_folder)

processor.plot_measurements(kind='background')
processor.plot_measurements(kind='sample')
processor.plot_measurements(kind='net')
plt.show()

# processor.export_table(kind='readings', folder_path=output_folder)
# processor.export_table(kind='background', folder_path=output_folder)
# processor.export_table(kind='sample', folder_path=output_folder)
# processor.export_table(kind='net', folder_path=output_folder)
# processor.export_table(kind='all', folder_path=output_folder)

# processor.export_plot(kind='background', folder_path=output_folder)
# processor.export_plot(kind='sample', folder_path=output_folder)
# processor.export_plot(kind='net', folder_path=output_folder)
