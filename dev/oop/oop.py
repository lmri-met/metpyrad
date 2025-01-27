import os
import shutil
from calendar import month_name

import matplotlib.pyplot as plt
import pandas as pd


def get_csv_files(folder_path):
    # List to store csv files with their full paths
    csv_files = []
    # Iterate over all the files in the given folder
    for file_name in os.listdir(folder_path):
        # Check if the file has a .csv extension
        if file_name.endswith('.csv'):
            # Append the absolute path of the file to the list
            csv_files.append(os.path.abspath(os.path.join(folder_path, file_name)))
    print(f'Found {len(csv_files)} CSV files in folder {folder_path}:')
    return csv_files


class DataProcessor:  # TODO: find a better name, use instrument model or something
    ROWS_TO_EXTRACT = ['Samp.', 'Repe.', 'CPM', 'Counts', 'DTime', 'Time', 'EndTime']
    DATE_TIME_FORMAT = '%d/%m/%Y %H:%M:%S'
    BLOCK_STARTER = 'Sample start'
    ID_LINES = 4
    DELIMITER = ';'

    def __init__(self, radionuclide, year, month):
        # There may be attributes for the radionuclide of the sample and the month and year of the measurement, for ID purposes
        self.radionuclide = radionuclide
        self.year = year
        self.month = month
        # A dataframe with the raw parsed values should be stored
        # This a dataframe with the parsed lines and computed values of live time and total counts value and uncertainties for the backgorund and the sample
        self.readings_df = None
        # Attributes dataframes may be one for the background, one for the sample, and one for the net quantities
        self.background_df = None
        self.sample_df = None
        self.net_df = None
        # Summary of the measurement
        self.summary_df = None
        self.number_of_cicles = None
        self.repetitions_per_cicle = None
        self.time_per_repetition = None
        self.number_of_measurements = None
        self.measurement_time = None

    def __repr__(self):
        return f'DataProcessor(radionuclide={self.radionuclide}, year={self.year}, month={self.month})'

    def __str__(self):
        msg = f'Measurements of {self.radionuclide} on {month_name[self.month]} {self.year}'
        attributes = ['number_of_cicles', 'repetitions_per_cicle', 'time_per_repetition', 'number_of_measurements',
                      'measurement_time']
        if all(getattr(self, attr) is not None for attr in attributes):
            msg += (f'\nNumber of cicles: {self.number_of_cicles}\n'
                    f'Repetitions per cicle:{self.repetitions_per_cicle}\n'
                    f'Time per repetition: {self.time_per_repetition} s\n'
                    f'Total number of measurements: {self.number_of_measurements}\n'
                    f'Total measurement time: {self.measurement_time} s')
        return msg

    def parse_csv_files(self, folder_path):
        input_files = get_csv_files(folder_path)
        extracted_data = []
        for file_number, input_file in enumerate(input_files, start=1):
            with open(input_file, 'r') as file:
                lines = file.readlines()
            current_block = {}
            for line in lines[self.ID_LINES:]:
                if line.strip() == 'Sample start':
                    if current_block:
                        extracted_data.append(current_block)
                    current_block = {'file': file_number}
                else:
                    for row in self.ROWS_TO_EXTRACT:
                        if line.startswith(row):
                            current_block[row] = line.split(self.DELIMITER)[1].strip()
            if current_block:
                extracted_data.append(current_block)
        df = pd.DataFrame(extracted_data, columns=self.ROWS_TO_EXTRACT + ['file'])
        for col in df.columns[:-2]:
            df[col] = pd.to_numeric(df[col])
        df[df.columns[-2]] = pd.to_datetime(df[df.columns[-2]], format=self.DATE_TIME_FORMAT)
        df = df.sort_values(by='EndTime')
        df = df.reset_index(drop=True)
        # Moving the last column to be the first
        cols = df.columns.tolist()
        cols = [cols[-1]] + cols[:-1]
        df = df[cols]
        # Rename columns
        old_names = ['file','Samp.','Repe.','CPM','Counts','DTime','Time','EndTime']
        new_names = ['Cicle','Sample','Repetitions','Count rate (cpm)','Counts (reading)','Dead time (s)','Real time (s)','End time']
        df = df.rename(columns=dict(zip(old_names, new_names)))
        self.readings_df = df

    def get_statistics(self):
        df = self.readings_df.copy()
        # Initialize a list to store the results
        results = []
        # Initialize a variable to store the total number of measurements
        total_measurements = 0
        # Iterate over each unique file
        for file_number in self.readings_df['Cicle'].unique():
            # Filter the DataFrame for the current file
            file_df = self.readings_df[self.readings_df['Cicle'] == file_number]
            # Get the maximum number of repetitions for the current file
            max_repetitions = file_df['Repetitions'].max()
            # Get the time for the repetitions (assuming it's the same for all repetitions of a single file)
            time_repetitions = file_df['Real time (s)'].iloc[0]
            # Check if all times are the same for the current file
            if not (file_df['Real time (s)'] == time_repetitions).all():
                raise ValueError(f'Time values are not consistent for file {file_number}')
            # Calculate the total number of measurements for the current file
            total_measurements += max_repetitions
            # Get the earliest end time for the current file
            earliest_end_time = file_df['End time'].min()
            # Append the results to the list
            results.append({
                'Cicle': file_number,
                'Repetitions': max_repetitions,
                'Real time (s)': time_repetitions,
                'Date': earliest_end_time
            })
        # Convert the results to a DataFrame
        self.summary_df = pd.DataFrame(results, columns=['Cicle', 'Repetitions', 'Real time (s)', 'Date'])
        # Get the number of unique files
        self.number_of_cicles = df['Cicle'].nunique()
        # Assing the total number of measurements
        self.number_of_measurements = self.summary_df['Repetitions'].sum()
        # Get the total measurement time
        self.measurement_time = (self.summary_df['Repetitions'] * self.summary_df['Real time (s)']).sum()
        # Get the time per repetition TODO: are these always the same?
        time_repetitions = self.summary_df['Real time (s)'].iloc[0]
        if not (self.summary_df['Real time (s)'] == time_repetitions).all():
            raise ValueError(f'Time values are not consistent for all files')
        self.time_per_repetition = time_repetitions
        # Get the repetitions per cicle TODO: are these always the same?
        repetitions_per_cicle = self.summary_df['Repetitions'].iloc[0]
        if not (self.summary_df['Repetitions'] == repetitions_per_cicle).all():
            raise ValueError(f'Repetitions per cicle are not consistent for all files')
        self.repetitions_per_cicle = repetitions_per_cicle

    def get_background_sample_df(self):
        df = self.readings_df.copy()
        df['Live time (s)'] = df['Real time (s)'] - df['Dead time (s)']
        df['Counts'] = df['Count rate (cpm)'] * df['Real time (s)'] / 60
        df['Counts uncertainty'] = df['Counts'].pow(1 / 2)
        df['Counts uncertainty (%)'] = df['Counts uncertainty'] / df['Counts'] * 100
        df_b = df[df['Sample'] == df['Sample'].unique()[0]].reset_index(drop=True)
        df_s = df[df['Sample'] == df['Sample'].unique()[1]].reset_index(drop=True)
        # TODO: drop unncessesary columns
        self.background_df = df_b
        self.sample_df = df_s

    def get_net_quantities_df(self, time_unit):  # TODO: check time conversion factors
        net_cpm = self.sample_df['Count rate (cpm)'] - self.background_df['Count rate (cpm)']
        net_counts = self.sample_df['Counts'] - self.background_df['Counts']
        u_net_counts = (self.sample_df['Counts uncertainty'].pow(2) + self.background_df['Counts uncertainty'].pow(2)).pow(1 / 2)
        ur_net_counts = u_net_counts / net_counts * 100
        initial_time = self.sample_df['End time'].min()
        elapsed_time = self.sample_df['End time'] - initial_time
        time_conversion = {'s': 1, 'min': 1 / 60, 'h': 1 / 3600, 'd': 1 / 86400, 'wk': 1 / (86400 * 7), 'mo': 1 / (86400 * 30.44), 'yr': 1 / (86400 * 365.25)}
        if time_unit not in time_conversion:
            raise ValueError(f'Invalid unit. Choose from seconds ("s"), minutes ("min"), hours ("h"), days ("d"), weeks ("wk"), months ("mo"), or years ("yr").')
        elapsed_time_unit = pd.Series([i.total_seconds() for i in elapsed_time]) * time_conversion[time_unit]
        labels = ['Elapsed time', f'Elapsed time ({time_unit})', 'Count rate (cpm)', 'Counts', 'Counts uncertainty', 'Counts uncertainty (%)']
        data = [elapsed_time, elapsed_time_unit, net_cpm, net_counts, u_net_counts, ur_net_counts]
        self.net_df = pd.DataFrame(dict(zip(labels, data)))

    def concatenate_results(self):
        # Sample DataFrames
        df1 = self.background_df.copy()
        df2 = self.sample_df.copy()
        df3 = self.net_df.copy()
        # Creating multi-level headers
        header1 = pd.MultiIndex.from_product([['Background'], df1.columns])
        header2 = pd.MultiIndex.from_product([['Sample'], df2.columns])
        header3 = pd.MultiIndex.from_product([['Net'], df3.columns])
        # Assigning the multi-level headers to the DataFrames
        df1.columns = header1
        df2.columns = header2
        df3.columns = header3
        # Concatenating the DataFrames
        return pd.concat([df1, df2, df3], axis=1)

    def plot_readings(self, sample):
        if sample == 'background':
            df = self.background_df
        elif sample == 'sample':
            df = self.sample_df
        else:
            raise ValueError('Invalid sample value. Choose from "background" or "sample".')
        x = df['End time']
        xlabel = 'End time'
        markersize = 2
        fig, axs = plt.subplots(3, 2, figsize=(2.5 * 8, 2 * 6), sharex=True)
        axs[0, 0].plot(x, df['Count rate (cpm)'], 'o-', markersize=markersize)
        axs[0, 0].set_ylabel('Count rate (cpm)')
        axs[0, 1].plot(x, df['Dead time (s)'], 'o-', markersize=markersize)
        axs[0, 1].set_ylabel('Dead time (s)')
        axs[1, 0].plot(x, df['Real time (s)'], 'o-', markersize=markersize)
        axs[1, 0].set_ylabel('Real time (s)')
        axs[1, 1].plot(x, df['Live time (s)'], 'o-', markersize=markersize)
        axs[1, 1].set_ylabel('Live time (s)')
        axs[2, 0].plot(x, df['Counts (reading)'], 'o-', label='Measured', markersize=markersize)
        axs[2, 0].plot(x, df['Counts'], 'o-', label='Calculated', markersize=markersize)
        axs[2, 0].set_ylabel('Counts')
        axs[2, 0].legend()
        axs[2, 0].set_xlabel(xlabel)
        axs[2, 0].tick_params(axis='x', rotation=45)
        axs[2, 1].plot(x, df['Counts uncertainty (%)'], 'o-', markersize=markersize)
        axs[2, 1].set_ylabel('Counts uncertainty (%)')
        axs[2, 1].set_xlabel(xlabel)
        axs[2, 1].tick_params(axis='x', rotation=45)
        fig.suptitle(f'{sample.capitalize()} measurements')
        plt.tight_layout()
        return fig

    def plot_net_quantities(self):
        df = self.net_df
        # Extracting the unit from the column label
        etime_column = [col for col in df.columns if col.startswith('Elapsed time (')][0]
        unit = etime_column.split('(')[-1].strip(')')
        x = df[f'Elapsed time ({unit})']
        xlabel = f'Elapsed time ({unit})'
        markersize = 2
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
        ax1.plot(x, df['Counts'], 'o-', markersize=markersize)
        ax1.set_ylabel('Counts')
        ax1.set_xlabel(xlabel)
        ax1.tick_params(axis='x', rotation=45)
        ax2.plot(x, df['Counts uncertainty (%)'], 'o-', markersize=markersize)
        ax2.set_ylabel('Counts uncertainty (%)')
        ax2.set_xlabel(xlabel)
        ax2.tick_params(axis='x', rotation=45)
        fig.suptitle(f'Net quantities measurements')
        plt.tight_layout()
        return fig

    def process_readings(self, folder_path, time_unit):
        output_folder = f'{self.radionuclide}_{self.year}_{self.month}'
        os.makedirs(output_folder, exist_ok=True)
        print(f'Processing readings from {folder_path}.')
        self.parse_csv_files(folder_path)
        self.get_statistics()
        self.get_background_sample_df()
        self.get_net_quantities_df(time_unit)
        df = self.concatenate_results()
        print(f'Saving CSV files to folder {output_folder}.')
        if os.path.exists(f'{output_folder}/readings'):
            shutil.rmtree(f'{output_folder}/readings')
        shutil.copytree(folder_path, f'{output_folder}/readings')
        self.background_df.to_csv(f'{output_folder}/background.csv', index=False)
        self.sample_df.to_csv(f'{output_folder}/sample.csv', index=False)
        self.net_df.to_csv(f'{output_folder}/net.csv', index=False)
        df.to_csv(f'{output_folder}/results.csv', index=False)
        print(f'Saving figures to folder {output_folder}.')
        fig1 = self.plot_readings('sample')
        plt.savefig(f'{output_folder}/sample_measurements.png')
        fig2 = self.plot_readings('background')
        plt.savefig(f'{output_folder}/background_measurements.png')
        fig3 = self.plot_net_quantities()
        plt.savefig(f'{output_folder}/net_quantities.png')
        print('Measurements summary:')
        print(processor)


if __name__ == "__main__":
    processor = DataProcessor(radionuclide='Lu-177', year=2023, month=11)
    input_folder_path = '../ref_case/equipment_output_files'
    processor.process_readings(input_folder_path, 's')
