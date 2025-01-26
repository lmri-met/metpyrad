import os
from calendar import month_name

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

    # print(f'Found {len(csv_files)} CSV files:')
    # for i in csv_files:
    #     print(i)

    return csv_files


class DataProcessor:#TODO: find a better name, use instrument model or something
    ROWS_TO_EXTRACT = ["Samp.", "Repe.", "CPM", "Counts", "DTime", "Time", "EndTime"]
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
        attributes = ['number_of_cicles', 'repetitions_per_cicle', 'time_per_repetition', 'number_of_measurements', 'measurement_time']
        if all(getattr(self, attr) is not None for attr in attributes):
            msg += (f'\nNumber of cicles: {self.number_of_cicles}\n'
                    f'Repetitions per cicle:{self.repetitions_per_cicle}\n'
                    f'Time per repetition: {self.time_per_repetition} s\n'
                    f'Total number of measurements: {self.number_of_measurements}\n'
                    f'Total measurement time: {self.measurement_time} s')

        return msg

    def parse_csv_files(self, input_files):
        extracted_data = []
        for file_number, input_file in enumerate(input_files, start=1):
            with open(input_file, 'r') as file:
                lines = file.readlines()
            current_block = {}
            for line in lines[self.ID_LINES:]:
                if line.strip() == "Sample start":
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
        self.readings_df = df

    def analyze_files(self):# TODO: find a better name
        df = self.readings_df

        # Initialize a list to store the results
        results = []

        # Initialize a variable to store the total number of measurements
        total_measurements = 0

        # Iterate over each unique file
        for file_number in self.readings_df['file'].unique():
            # Filter the DataFrame for the current file
            file_df = self.readings_df[self.readings_df['file'] == file_number]

            # Get the maximum number of repetitions for the current file
            max_repetitions = file_df['Repe.'].max()

            # Get the time for the repetitions (assuming it's the same for all repetitions of a single file)
            time_repetitions = file_df['Time'].iloc[0]

            # Check if all times are the same for the current file
            if not (file_df['Time'] == time_repetitions).all():
                raise ValueError(f"Time values are not consistent for file {file_number}")

            # Calculate the total number of measurements for the current file
            total_measurements += max_repetitions

            # Get the earliest end time for the current file
            earliest_end_time = file_df['EndTime'].min()

            # Append the results to the list
            results.append({
                'File': file_number,
                'Repetitions': max_repetitions,
                'Time': time_repetitions,
                'Date': earliest_end_time
            })

        # Convert the results to a DataFrame
        self.summary_df = pd.DataFrame(results, columns=['File', 'Repetitions', 'Time', 'Date'])
        # Get the number of unique files
        self.number_of_cicles = df['file'].nunique()
        # Assing the total number of measurements
        self.number_of_measurements = self.summary_df['Repetitions'].sum()
        # Get the total measurement time
        self.measurement_time = (self.summary_df['Repetitions'] * self.summary_df['Time']).sum()

        time_repetitions = self.summary_df['Time'].iloc[0]
        if not (self.summary_df['Time'] == time_repetitions).all():
            raise ValueError(f"Time values are not consistent for all files")
        self.time_per_repetition = time_repetitions

        repetitions_per_cicle = self.summary_df['Repetitions'].iloc[0]
        if not (self.summary_df['Repetitions'] == repetitions_per_cicle).all():
            raise ValueError(f"Repetitions per cicle are not consistent for all files")
        self.repetitions_per_cicle = repetitions_per_cicle

    def get_background_sample_df(self):
        df = self.readings_df
        df["LTime"] = df["Time"] - df["DTime"]
        df["Counts_"] = df["CPM"] * df["Time"] / 60
        df["UCounts"] = df["Counts_"].pow(1 / 2)
        df["UrCounts"] = df["UCounts"] / df["Counts_"] * 100

        df_b = df[df["Samp."] == df["Samp."].unique()[0]].reset_index(drop=True)
        df_s = df[df["Samp."] == df["Samp."].unique()[1]].reset_index(drop=True)
        # TODO: drop unncessesary columns
        self.background_df = df_b
        self.sample_df = df_s



if __name__ == "__main__":
    input_csv_files = get_csv_files(folder_path='../ref_case/equipment_output_files')

    processor = DataProcessor(radionuclide='Lu-177', year=2023, month=11)

    print(processor)
    print(repr(processor))

    processor.parse_csv_files(input_csv_files)
    processor.analyze_files()
    processor.get_background_sample_df()

    print(processor)
