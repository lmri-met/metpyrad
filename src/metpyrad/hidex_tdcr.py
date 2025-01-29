import os
import shutil
from calendar import month_name

import matplotlib.pyplot as plt
import pandas as pd


class HidexTDCRProcessor:
    """A class to process and summarize measurements for a given radionuclide with a Hidex TDCR.

    Attributes:
        radionuclide (str): Name of the radionuclide being measured.
        year (int): Year of the measurements.
        month (int): Month of the measurements.
        readings (pd.DataFrame or None): DataFrame containing the readings.
        background (pd.DataFrame or None): DataFrame containing the background measurements.
        sample (pd.DataFrame or None): DataFrame containing the sample measurements.
        net (pd.DataFrame or None): DataFrame containing the net measurements.
        measurements (pd.DataFrame or None): DataFrame containing all measurements.
        summary (str or None): A summary of the measurements.
        cycles (int or None): Number of cycles in the measurements.
        cycle_repetitions (int or None): Number of repetitions per cycle.
        repetition_time (float or None): Time per repetition in seconds.
        total_measurements (int or None): Total number of measurements.
        measurement_time (float or None): Total measurement time in seconds.
    """
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
    # Identifier for background measurements in the CSV files
    _BACKGROUND_ID = 1
    # Identifier for sample measurements in the CSV files
    _SAMPLE_ID = 2

    def __init__(self, radionuclide, year, month):
        """Initializes the HidexTDCRProcessor with the given radionuclide, year, and month.

        Args:
            radionuclide (str): Name of the radionuclide being measured.
            year (int): Year of the measurements.
            month (int): Month of the measurements.
        """
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
        """Returns a string representation of the HidexTDCRProcessor object, summarizing the measurements.

        Returns:
            str: A string summarizing the measurements of the radionuclide for the specified month and year.
                 If all relevant attributes are not None, includes detailed summary information.

        Example:
            >>> processor = HidexTDCRProcessor('Lu-177', 2023, 11)
            >>> print(processor)
            Measurements of Lu-177 on November 2023
        """
        # Create the initial message with the radionuclide and date information
        msg = f'Measurements of {self.radionuclide} on {month_name[self.month]} {self.year}'
        # List of attributes to check for completeness of the summary
        attributes = ['cycles', 'cycle_repetitions', 'repetition_time', 'measurements', 'measurement_time', 'summary']
        # If all relevant attributes are not None, add detailed summary information
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
        """
        Summarizes the readings by printing the string representation of the object.
        Optionally saves the summary to a text file.

        Args:
            save (bool): If True, saves the summary to a text file. Default is False.
            folder_path (str): Path to the folder where the summary file will be saved. Required if save is True.

        Returns:
            None

        Example:
            >>> processor = HidexTDCRProcessor('Lu-177', 2023, 11)
            >>> processor.summarize_readings()
            Measurements of Lu-177 on November 2023
            ...
            >>> processor.summarize_readings(save=True, folder_path='/path/to/folder')
            Measurements of Lu-177 on November 2023
            Summary saved to /path/to/folder/summary.txt
        """
        # Print the string representation of the object
        print(self.__str__())

        # If save is True, save the summary to a text file
        if save:
            # Open the file in write mode
            with open(f'{folder_path}/summary.txt', 'w') as file:
                # Write the string representation of the object to the file
                file.write(self.__str__())
            print(f'Summary saved to {folder_path}/summary.txt')

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
        input_files = _get_csv_files(folder_path)
        extracted_data = []

        for file_number, input_file in enumerate(input_files, start=1):
            with open(input_file, 'r') as file:
                lines = file.readlines()
            current_block = {}
            for line in lines[self._ID_LINES:]:
                if line.strip() == 'Sample start':
                    if current_block:
                        extracted_data.append(current_block)
                    current_block = {'file': file_number}
                else:
                    for row in self._ROWS_TO_EXTRACT:
                        if line.startswith(row):
                            current_block[row] = line.split(self._DELIMITER)[1].strip()
            if current_block:
                extracted_data.append(current_block)

        df = pd.DataFrame(extracted_data, columns=self._ROWS_TO_EXTRACT + ['file'])

        for col in df.columns[:-2]:
            df[col] = pd.to_numeric(df[col])
        df[df.columns[-2]] = pd.to_datetime(df[df.columns[-2]], format=self._DATE_TIME_FORMAT)

        # Sort by date time
        df = df.sort_values(by='EndTime')
        df = df.reset_index(drop=True)

        # Reassign values to files according to chronological order
        value_counts = df['file'].value_counts()
        if not value_counts.nunique() == 1:
            raise ValueError('Repetitions per cycle are not consistent for all measurements.')
        df['file'] = [i for i in range(1, df['file'].unique().size + 1) for _ in range(value_counts.unique()[0])]

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
            ids = {'background': self._BACKGROUND_ID, 'sample': self._SAMPLE_ID}
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
        """Plots the specified type of measurements.

        Args:
            kind (str): The type of measurements to plot. Options are 'background', 'sample', or 'net'.

        Returns:
            None

        Raises:
            ValueError: If an invalid measurement kind is provided.

        Example:
            >>> processor = HidexTDCRProcessor('Lu-177', 2023, 11)
            >>> processor.parse_readings('/path/to/folder')
            >>> processor.process_readings('all')
            >>> processor.plot_measurements('net')
        """
        # Check the kind of measurements to plot
        if kind == 'background':
            # Plot background measurements
            _plot_background_sample_measurements(df=self.background, kind=kind)
        elif kind == 'sample':
            # Plot sample measurements
            _plot_background_sample_measurements(df=self.sample, kind=kind)
        elif kind == 'net':
            # Plot net measurements
            _plot_net_measurements(df=self.net)
        else:
            # Raise an error if the kind is invalid
            raise ValueError(f'Invalid measurement kind. Choose from "background", "sample", or "net".')

    def export_measurements_table(self, kind, folder_path):
        """Exports the specified type of measurements to a CSV file.

        Args:
            kind (str): The type of measurements to export. Options are 'readings', 'background', 'sample', 'net', or 'all'.
            folder_path (str): The path to the folder where the CSV file will be saved.

        Returns:
            None

        Raises:
            ValueError: If an invalid measurement kind is provided.

        Example:
            >>> processor = HidexTDCRProcessor('Lu-177', 2023, 11)
            >>> processor.parse_readings('/path/to/folder')
            >>> processor.process_readings('all')
            >>> processor.export_measurements_table('net', '/path/to/folder')
        """
        # Dictionary mapping measurement kinds to their corresponding DataFrames
        dfs = {
            'readings': self.readings,
            'background': self.background,
            'sample': self.sample,
            'net': self.net,
            'all': self._compile_measurements()
        }
        # Check if the provided kind is valid
        if kind not in dfs.keys():
            raise ValueError(f'Invalid measurement kind. Choose from "readings", "background", "sample", "net", or "all".')
        # Export the specified DataFrame to a CSV file
        dfs[kind].to_csv(f'{folder_path}/{kind}.csv', index=False)

    def export_measurements_plot(self, kind, folder_path):
        """Exports the specified type of measurement plot to a PNG file.

        Args:
            kind (str): The type of measurements to plot. Options are 'background', 'sample', or 'net'.
            folder_path (str): The path to the folder where the PNG file will be saved.

        Returns:
            None

        Raises:
            ValueError: If an invalid measurement kind is provided.

        Example:
            >>> processor = HidexTDCRProcessor('Lu-177', 2023, 11)
            >>> processor.parse_readings('/path/to/folder')
            >>> processor.process_readings('all')
            >>> processor.export_measurements_plot('net', '/path/to/folder')
        """
        # Dictionary mapping measurement kinds to their corresponding DataFrames
        dfs = {
            'background': self.background,
            'sample': self.sample,
            'net': self.net
        }
        # Check if the provided kind is valid
        if kind not in dfs.keys():
            raise ValueError(f'Invalid measurement kind. Choose from "background", "sample", or "net".')
        # Plot the specified measurements
        self.plot_measurements(kind=kind)
        # Save the plot to a PNG file
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


def _get_csv_files(folder_path):
    """Retrieves a list of CSV files from the specified folder.

    Args:
        folder_path (str): The path to the folder containing the files.

    Returns:
        list: A list of full paths to the CSV files found in the folder.

    Example:
        >>> _get_csv_files('/path/to/folder')
        Found 3 CSV files in folder /path/to/folder:
        ['/path/to/folder/file1.csv', '/path/to/folder/file2.csv', '/path/to/folder/file3.csv']
    """
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


def _get_elapsed_time(df, time_unit='s'):
    """Calculate the elapsed time from the minimum 'End time' in a dataframe and convert it to the specified time unit.

    Args:
        df (pd.DataFrame): DataFrame containing a column 'End time' with datetime values.
        time_unit (str): The unit of time to convert the elapsed time to.
                         Options are 's' (seconds), 'min' (minutes), 'h' (hours), 'd' (days),
                         'wk' (weeks), 'mo' (months), 'yr' (years). Default is 's'.

    Returns:
        tuple: A tuple containing:
            - pd.Series: Elapsed time in the original time delta format.
            - pd.Series: Elapsed time converted to the specified time unit.

    Raises:
        ValueError: If an invalid time unit is provided.

    Example:
        >>> df = pd.DataFrame({'End time': pd.to_datetime(['2023-11-30 08:44:20', '2023-12-01 12:46:16'])})
        >>> elapsed_time, elapsed_time_unit = _get_elapsed_time(df, time_unit='h')
        >>> print(elapsed_time)
        0   0 days 00:00:00
        1   1 days 04:01:56
        Name: End time, dtype: timedelta64[ns]
        >>> print(elapsed_time_unit)
        0     0.000000
        1    28.032222
        dtype: float64
    """
    # Find the earliest 'End time' in the DataFrame
    initial_time = df['End time'].min()
    # Calculate the elapsed time from the initial time for each entry
    elapsed_time = df['End time'] - initial_time
    # Define conversion factors for different time units
    time_conversion = {
        's': 1,  # seconds
        'min': 1 / 60,  # minutes
        'h': 1 / 3600,  # hours
        'd': 1 / 86400,  # days
        'wk': 1 / (86400 * 7),  # weeks
        'mo': 1 / (86400 * 30.44),  # months (approximate)
        'yr': 1 / (86400 * 365.25)  # years (approximate)
    }
    # Check if the provided time unit is valid
    if time_unit not in time_conversion:
        raise ValueError(f'Invalid unit. Choose from seconds ("s"), minutes ("min"), hours ("h"), days ("d"), '
                         f'weeks ("wk"), months ("mo"), or years ("yr").')
    # Convert elapsed time to the specified unit
    elapsed_time_unit = pd.Series([i.total_seconds() for i in elapsed_time]) * time_conversion[time_unit]
    return elapsed_time, elapsed_time_unit


def _plot_background_sample_measurements(df, kind):
    """Plots various quantities for background or sample measurements from the given DataFrame.

    Args:
        df (pd.DataFrame): DataFrame containing the measurement data with columns 'End time', 'Count rate (cpm)',
                           'Dead time', 'Real time (s)', 'Live time (s)', 'Counts (reading)', 'Counts', and 'Counts uncertainty (%)'.
        kind (str): A string indicating the type of measurements (e.g., 'background' or 'sample').

    Returns:
        matplotlib.figure.Figure: The figure object containing the plots.

    Example:
        >>> df = pd.DataFrame({
        ...     'End time': pd.to_datetime(['2023-11-30 08:44:20', '2023-12-01 12:46:16']),
        ...     'Count rate (cpm)': [100, 150],
        ...     'Dead time': [0.1, 0.2],
        ...     'Real time (s)': [60, 120],
        ...     'Live time (s)': [50, 110],
        ...     'Counts (reading)': [5000, 7500],
        ...     'Counts': [4950, 7400],
        ...     'Counts uncertainty (%)': [1.0, 1.2]
        ... })
        >>> fig = _plot_background_sample_measurements(df, 'background')
        >>> plt.show()
        """
    # Extract the 'End time' column for the x-axis
    x = df['End time']
    xlabel = 'End time'
    markersize = 2
    # Create a 3x2 grid of subplots
    fig, axs = plt.subplots(3, 2, figsize=(2.5 * 8, 2 * 6), sharex=True)
    # Plot 'Count rate (cpm)' on the first subplot
    axs[0, 0].plot(x, df['Count rate (cpm)'], 'o-', markersize=markersize)
    axs[0, 0].set_ylabel('Count rate (cpm)')
    # Plot 'Dead time' on the second subplot
    axs[0, 1].plot(x, df['Dead time'], 'o-', markersize=markersize)
    axs[0, 1].set_ylabel('Dead time')
    # Plot 'Real time (s)' on the third subplot
    axs[1, 0].plot(x, df['Real time (s)'], 'o-', markersize=markersize)
    axs[1, 0].set_ylabel('Real time (s)')
    # Plot 'Live time (s)' on the fourth subplot
    axs[1, 1].plot(x, df['Live time (s)'], 'o-', markersize=markersize)
    axs[1, 1].set_ylabel('Live time (s)')
    # Plot 'Counts (reading)' and 'Counts' on the fifth subplot
    axs[2, 0].plot(x, df['Counts (reading)'], 'o-', label='Measured', markersize=markersize)
    axs[2, 0].plot(x, df['Counts'], 'o-', label='Calculated', markersize=markersize)
    axs[2, 0].set_ylabel('Counts')
    axs[2, 0].legend()
    axs[2, 0].set_xlabel(xlabel)
    axs[2, 0].tick_params(axis='x', rotation=45)
    # Plot 'Counts uncertainty (%)' on the sixth subplot
    axs[2, 1].plot(x, df['Counts uncertainty (%)'], 'o-', markersize=markersize)
    axs[2, 1].set_ylabel('Counts uncertainty (%)')
    axs[2, 1].set_xlabel(xlabel)
    axs[2, 1].tick_params(axis='x', rotation=45)
    # Set the overall title for the figure
    fig.suptitle(f'{kind.capitalize()} measurements')
    # Adjust the layout to prevent overlap
    plt.tight_layout()
    return fig


def _plot_net_measurements(df):
    """Plots various quantities for net measurements from the given DataFrame.

    Args:
        df (pd.DataFrame): DataFrame containing the measurement data with columns 'Elapsed time (unit)',
                           'Counts', and 'Counts uncertainty (%)'.

    Returns:
        matplotlib.figure.Figure: The figure object containing the plots.

    Example:
        >>> df = pd.DataFrame({
        ...     'Elapsed time (s)': [0, 10, 20, 30],
        ...     'Counts': [100, 150, 200, 250],
        ...     'Counts uncertainty (%)': [1.0, 1.2, 1.1, 1.3]
        ... })
        >>> fig = _plot_net_measurements(df)
        >>> plt.show()
    """
    # Extracting the unit from the column label
    etime_column = [col for col in df.columns if col.startswith('Elapsed time (')][0]
    unit = etime_column.split('(')[-1].strip(')')
    # Extract the 'Elapsed time' column for the x-axis
    x = df[f'Elapsed time ({unit})']
    xlabel = f'Elapsed time ({unit})'
    markersize = 2
    # Create a 2x1 grid of subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
    # Plot 'Counts' on the first subplot
    ax1.plot(x, df['Counts'], 'o-', markersize=markersize)
    ax1.set_ylabel('Counts')
    ax1.set_xlabel(xlabel)
    ax1.tick_params(axis='x', rotation=45)
    # Plot 'Counts uncertainty (%)' on the second subplot
    ax2.plot(x, df['Counts uncertainty (%)'], 'o-', markersize=markersize)
    ax2.set_ylabel('Counts uncertainty (%)')
    ax2.set_xlabel(xlabel)
    ax2.tick_params(axis='x', rotation=45)
    # Set the overall title for the figure
    fig.suptitle('Net quantities measurements')
    # Adjust the layout to prevent overlap
    plt.tight_layout()
    return fig
