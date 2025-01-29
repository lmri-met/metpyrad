import os
import shutil
from calendar import month_name

import matplotlib.pyplot as plt
import pandas as pd


class HidexTDCRProcessor:
    ROWS_TO_EXTRACT = ['Samp.', 'Repe.', 'CPM', 'Counts', 'DTime', 'Time', 'EndTime']
    DATE_TIME_FORMAT = '%d/%m/%Y %H:%M:%S'
    BLOCK_STARTER = 'Sample start'
    ID_LINES = 4
    DELIMITER = ';'
    BACKGROUND_ID = 1
    SAMPLE_ID = 2

    def __init__(self, radionuclide, year, month):
        self.radionuclide = radionuclide
        self.year = year
        self.month = month
        self.readings = None
        self.background = None
        self.sample = None
        self.net = None
        self.measurements = None
        self.summary = None
        self.cycles = None
        self.cycle_repetitions = None
        self.repetition_time = None
        self.total_measurements = None
        self.measurement_time = None

    def __repr__(self):
        return f'DataProcessor(radionuclide={self.radionuclide}, year={self.year}, month={self.month})'

    def __str__(self):
        msg = f'Measurements of {self.radionuclide} on {month_name[self.month]} {self.year}'
        attributes = ['cycles', 'cycle_repetitions', 'repetition_time', 'measurements', 'measurement_time', 'summary']
        if all(getattr(self, attr) is not None for attr in attributes):
            msg += (f'\nSummary\n'
                    f'Number of cycles: {self.cycles}\n'
                    f'Repetitions per cycle: {self.cycle_repetitions}\n'
                    f'Time per repetition: {self.repetition_time} s\n'
                    f'Total number of measurements: {self.total_measurements}\n'
                    f'Total measurement time: {self.measurement_time} s\n'
                    f'Cycles summary\n'
                    f'{self.summary}')
        return msg

    def parse_readings(self, folder_path):
        self.readings = self._parse_readings(folder_path=folder_path)
        self.summary = self._get_readings_summary()
        statistics = self._get_readings_statistics()
        self.cycles = statistics['cycles']
        self.cycle_repetitions = statistics['cycle_repetitions']
        self.repetition_time = statistics['repetition_time']
        self.total_measurements = statistics['measurements']
        self.measurement_time = statistics['measurement_time']

    def summarize_readings(self, save=False, folder_path=None):
        print(self.__str__())
        if save:
            with open(f'{folder_path}/summary.txt', 'w') as file:
                file.write(self.__str__())

    def process_readings(self, kind, time_unit='s'):
        if kind == 'background':
            self.background = self._get_background_sample(kind='background', time_unit=time_unit)
        elif kind == 'sample':
            self.sample = self._get_background_sample(kind='sample', time_unit=time_unit)
        elif kind == 'net':
            self.net = self._get_net_measurements(time_unit=time_unit)
        elif kind == 'all':
            self.background = self._get_background_sample(kind='background', time_unit=time_unit)
            self.sample = self._get_background_sample(kind='sample', time_unit=time_unit)
            self.net = self._get_net_measurements(time_unit=time_unit)
            self.measurements = self._compile_measurements()
        else:
            raise ValueError(f'Invalid measurement kind. Choose from "background", "sample", "net" or "all".')

    def _parse_readings(self, folder_path):
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
        old_names = ['file', 'Samp.', 'Repe.', 'CPM', 'Counts', 'DTime', 'Time', 'EndTime']
        new_names = ['Cycle', 'Sample', 'Repetitions', 'Count rate (cpm)', 'Counts (reading)', 'Dead time',
                     'Real time (s)', 'End time']
        df = df.rename(columns=dict(zip(old_names, new_names)))
        return df

    def _get_readings_summary(self):
        if self.readings is not None:
            # Check if real times are the same for all files
            if not self.readings['Real time (s)'].nunique() == 1:
                raise ValueError('Real time values are not consistent for all measurements. Check readings table.')
            # Initialize a list to store the results
            results = []
            # Iterate over each unique file
            for cycle in self.readings['Cycle'].unique():
                # Filter the DataFrame for the current file
                df = self.readings[self.readings['Cycle'] == cycle]
                # Get the maximum number of repetitions for the current file
                repetitions = df['Repetitions'].max()
                # Get the time for the repetitions (assuming it's the same for all repetitions of a single file)
                real_time = df['Real time (s)'].iloc[0]
                # Get the earliest end time for the current file
                start_time = df['End time'].min()
                # Append the results to the list
                results.append({'Cycle': cycle, 'Repetitions': repetitions, 'Real time (s)': real_time, 'Date': start_time})
            # Convert the results to a DataFrame
            return pd.DataFrame(results, columns=['Cycle', 'Repetitions', 'Real time (s)', 'Date'])
        else:
            raise ValueError('No readings data to compute readings summary. Please read the CSV files first.')

    def _get_readings_statistics(self):
        if self.summary is not None:
            # Check if repetitions per cycle are the same for all files
            if not self.summary['Repetitions'].nunique() == 1:
                raise ValueError('Repetitions per cycle are not consistent for all measurements. Check summary table.')
            # Get the number of unique files
            cycles = self.summary['Cycle'].count()
            # Assign the total number of measurements
            measurements = self.summary['Repetitions'].sum()
            # Get the total measurement time
            measurement_time = (self.summary['Repetitions'] * self.summary['Real time (s)']).sum()
            # Get the time per repetition
            repetition_time = self.summary['Real time (s)'].iloc[0]
            # Get the repetitions per Cycle
            cycle_repetitions = self.summary['Repetitions'].iloc[0]
            # Create a dictionary to store results
            labels = ['cycles', 'cycle_repetitions', 'repetition_time', 'measurements', 'measurement_time']
            values = [cycles, cycle_repetitions, repetition_time, measurements, measurement_time]
            statistics = dict(zip(labels, values))
            return statistics
        else:
            raise ValueError('No readings summary data to compute readings statistics. Please get the readings summary.')

    def _get_background_sample(self, kind, time_unit='s'):
        # TODO: dead time is a factor o a number in seconds?
        if self.readings is not None:
            ids = {'background': self.BACKGROUND_ID, 'sample': self.SAMPLE_ID}
            df = self.readings.copy()
            df = df[df['Sample'] == ids[kind]].reset_index(drop=True)
            elapsed_time, elapsed_time_unit = _get_elapsed_time(df, time_unit)
            df['Live time (s)'] = df['Real time (s)'] / df['Dead time']
            df['Elapsed time'] = elapsed_time
            df[f'Elapsed time ({time_unit})'] = elapsed_time_unit
            df['Counts'] = df['Count rate (cpm)'] * df['Live time (s)'] / 60
            df['Counts uncertainty'] = df['Counts'].pow(1 / 2)
            df['Counts uncertainty (%)'] = df['Counts uncertainty'] / df['Counts'] * 100
            return df
        else:
            raise ValueError(f'No readings data to compute {kind} measurements. Please read the CSV files first.')

    def _get_net_measurements(self, time_unit='s'):
        # TODO: check time conversion factors
        if self.background is not None and self.sample is not None:
            data = {'Cycle': self.sample['Cycle'], 'Repetitions': self.sample['Repetitions'],
                'Elapsed time': self.sample['Elapsed time'],
                f'Elapsed time ({time_unit})': self.sample[f'Elapsed time ({time_unit})'],
                'Count rate (cpm)': self.sample['Count rate (cpm)'] - self.background['Count rate (cpm)'],
                'Counts': self.sample['Counts'] - self.background['Counts'],
                'Counts uncertainty': (self.sample['Counts'] + self.background['Counts']).pow(1 / 2), }
            data['Counts uncertainty (%)'] = data['Counts uncertainty'] / data['Counts'] * 100
            return pd.DataFrame(data)
        else:
            raise ValueError(f'No background and sample data to compute net measurements. Please process the readings first.')

    def _compile_measurements(self):
        if self.background is not None and self.sample is not None and self.net is not None:
            # Sample DataFrames
            df1 = self.background.copy()
            df2 = self.sample.copy()
            df3 = self.net.copy()
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
        else:
            raise ValueError(f'No background, sample and net data to compile measurements. Please process the readings first.')

    def plot_measurements(self, kind):
        if kind == 'background':
            _plot_background_sample_measurements(df=self.background, kind=kind)
        elif kind == 'sample':
            _plot_background_sample_measurements(df=self.sample, kind=kind)
        elif kind == 'net':
            _plot_net_measurements(df=self.net)
        else:
            raise ValueError(f'Invalid measurement kind. Choose from "background", "sample" or "net".')

    def export_measurements_table(self, kind, folder_path):
        dfs = {'readings': self.readings, 'background': self.background, 'sample': self.sample, 'net': self.net,
               'all': self._compile_measurements()}
        if kind not in dfs.keys():
            raise ValueError(f'Invalid measurement kind. Choose from "readings", "background", "sample" or "net".')
        dfs[kind].to_csv(f'{folder_path}/{kind}.csv', index=False)

    def export_measurements_plot(self, kind, folder_path):
        dfs = {'background': self.background, 'sample': self.sample, 'net': self.net}
        if kind not in dfs.keys():
            raise ValueError(f'Invalid measurement kind. Choose from "background", "sample" or "net".')
        self.plot_measurements(kind=kind)
        plt.savefig(f'{folder_path}/{kind}.png')

    def analyze_readings(self, input_folder, time_unit, save=False, output_folder=None):
        print(f'Processing readings from {input_folder}.')
        self.parse_readings(input_folder)
        self.process_readings(kind='all', time_unit=time_unit)
        print('Measurements summary:')
        print(self)
        if save:
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            folder = f'{output_folder}/{self.radionuclide}_{self.year}_{self.month}'
            print(f'Saving measurement files to folder {folder}.')
            if os.path.exists(folder):
                shutil.rmtree(folder)
            os.makedirs(folder)
            print('Saving CSV files')
            shutil.copytree(input_folder, f'{folder}/readings')
            self.export_measurements_table(kind='readings', folder_path=folder)
            self.export_measurements_table(kind='background', folder_path=folder)
            self.export_measurements_table(kind='sample', folder_path=folder)
            self.export_measurements_table(kind='net', folder_path=folder)
            self.export_measurements_table(kind='all', folder_path=folder)
            self.summarize_readings(save=True, folder_path=folder)
            print(f'Saving figures')
            self.export_measurements_plot(kind='background', folder_path=folder)
            self.export_measurements_plot(kind='sample', folder_path=folder)
            self.export_measurements_plot(kind='net', folder_path=folder)


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


def _get_elapsed_time(df, time_unit):
    initial_time = df['End time'].min()
    elapsed_time = df['End time'] - initial_time
    time_conversion = {'s': 1, 'min': 1 / 60, 'h': 1 / 3600, 'd': 1 / 86400, 'wk': 1 / (86400 * 7),
                       'mo': 1 / (86400 * 30.44), 'yr': 1 / (86400 * 365.25)}
    if time_unit not in time_conversion:
        raise ValueError(
            f'Invalid unit. Choose from seconds ("s"), minutes ("min"), hours ("h"), days ("d"), weeks ("wk"), months ("mo"), or years ("yr").')
    elapsed_time_unit = pd.Series([i.total_seconds() for i in elapsed_time]) * time_conversion[time_unit]
    return elapsed_time, elapsed_time_unit


def _plot_background_sample_measurements(df, kind):
    x = df['End time']
    xlabel = 'End time'
    markersize = 2
    fig, axs = plt.subplots(3, 2, figsize=(2.5 * 8, 2 * 6), sharex=True)
    axs[0, 0].plot(x, df['Count rate (cpm)'], 'o-', markersize=markersize)
    axs[0, 0].set_ylabel('Count rate (cpm)')
    axs[0, 1].plot(x, df['Dead time'], 'o-', markersize=markersize)
    axs[0, 1].set_ylabel('Dead time')
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
    fig.suptitle(f'{kind.capitalize()} measurements')
    plt.tight_layout()
    return fig


def _plot_net_measurements(df):
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
