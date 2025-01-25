# Refactor the script to functions

To simplify testing and improve the organization of the script, you can divide it into several functions, each responsible for a specific task. Here's how you can structure the script:

1. **Function to Parse CSV Files**:
   - This function will read the CSV files and extract the required rows.

2. **Function to Compute Quantities for Each Measurement**:
   - This function will compute the live time, total counts, and their uncertainties.

3. **Function to Transform the DataFrame Based on Measurement Types**:
   - This function will split the DataFrame into background and sample measurements, rename columns, and concatenate the DataFrames.

4. **Function to Compute Net Quantities**:
   - This function will calculate the net count rate, net counts, and their uncertainties.

5. **Function to Compute Elapsed Time**:
   - This function will compute the elapsed time in the specified unit.

6. **Main Function**:
   - This function will call the other functions and handle the overall workflow.

Here's how you can implement these functions:

```python
import pandas as pd

def parse_csv_files(input_files, rows_to_extract):
    extracted_data = []
    for input_file in input_files:
        with open(input_file, 'r') as file:
            lines = file.readlines()
        current_block = {}
        for line in lines[4:]:
            if line.strip() == "Sample start":
                if current_block:
                    extracted_data.append(current_block)
                current_block = {}
            else:
                for row in rows_to_extract:
                    if line.startswith(row):
                        current_block[row] = line.split(";")[1].strip()
        if current_block:
            extracted_data.append(current_block)
    df = pd.DataFrame(extracted_data, columns=rows_to_extract)
    for col in df.columns[:-1]:
        df[col] = pd.to_numeric(df[col])
    df[df.columns[-1]] = pd.to_datetime(df[df.columns[-1]], format='%d/%m/%Y %H:%M:%S')
    return df

def compute_quantities(df):
    df["LTime"] = df["Time"] - df["DTime"]
    df["Counts_"] = df["CPM"] * df["Time"] / 60
    df["UCounts"] = df["Counts_"].pow(1/2)
    df["UrCounts"] = df["UCounts"] / df["Counts_"] * 100
    return df

def transform_dataframe(df):
    df_b = df[df["Samp."] == df["Samp."].unique()[0]].reset_index(drop=True)
    df_s = df[df["Samp."] == df["Samp."].unique()[1]].reset_index(drop=True)
    df_b.columns = [col + "_bkgd" for col in df_b.columns]
    df_s.columns = [col + "_smpl" for col in df_s.columns]
    result_df = pd.concat([df_b, df_s], axis=1)
    result_df = result_df.drop(['Samp._bkgd', 'Samp._smpl', 'Repe._smpl'], axis=1)
    result_df = result_df.rename(columns={'Repe._bkgd': 'Repe.'})
    return result_df

def compute_net_quantities(result_df):
    result_df["CPM_net"] = result_df["CPM_smpl"] - result_df["CPM_bkgd"]
    result_df["Counts_net"] = result_df["Counts__smpl"] - result_df["Counts__bkgd"]
    result_df["UCounts_net"] = (result_df["UCounts_smpl"].pow(2) + result_df["UCounts_bkgd"].pow(2)).pow(1/2)
    result_df["UrCounts_net"] = result_df["UCounts_net"] / result_df["Counts_net"] * 100
    return result_df

def compute_elapsed_time(result_df, unit):
    initial_time = result_df['EndTime_smpl'].min()
    result_df['ETime'] = result_df['EndTime_smpl'] - initial_time
    label = f'ETime ({unit})'
    time_conversion = {
        'seconds': 1, 'minutes': 1/60, 'hours': 1/3600, 'days': 1/86400,
        'weeks': 1/(86400 * 7), 'months': 1/(86400 * 30.44), 'years': 1/(86400 * 365.25)
    }
    if unit not in time_conversion:
        raise ValueError("Invalid unit. Choose from 'seconds', 'minutes', 'hours', 'days', 'weeks', 'months', or 'years'.")
    elapsed_seconds = pd.Series([i.total_seconds() for i in result_df['ETime']]) * time_conversion[unit]
    result_df[label] = elapsed_seconds
    return result_df

def main():
    rows_to_extract = ["Samp.", "Repe.", "CPM", "Counts", "DTime", "Time", "EndTime"]
    input_files = ['csv_type1_1.csv', 'csv_type1_2.csv']
    
    # Step 1: Parse CSV files
    df = parse_csv_files(input_files, rows_to_extract)
    
    # Step 2: Compute quantities for each measurement
    df = compute_quantities(df)
    
    # Step 3: Transform the DataFrame based on measurement types
    result_df = transform_dataframe(df)
    
    # Step 4: Compute net quantities
    result_df = compute_net_quantities(result_df)
    
    # Step 5: Compute elapsed time
    unit = 'minutes'  # Change this to the desired unit
    result_df = compute_elapsed_time(result_df, unit)
    
    # Save the results
    df.to_csv('output1.csv', index=False)
    result_df.to_csv('output2.csv', index=False)
    print("Data extracted, types converted, and saved to output.csv")

if __name__ == "__main__":
    main()
```

### Explanation:
1. **`parse_csv_files`**: Reads and processes the CSV files to extract the required rows and convert data types.
2. **`compute_quantities`**: Computes live time, total counts, and their uncertainties.
3. **`transform_dataframe`**: Splits the DataFrame into background and sample measurements, renames columns, and concatenates the DataFrames.
4. **`compute_net_quantities`**: Calculates net count rate, net counts, and their uncertainties.
5. **`compute_elapsed_time`**: Computes the elapsed time in the specified unit.
6. **`main`**: Orchestrates the workflow by calling the other functions and saving the results.

This structure makes it easier to test each function individually and ensures that the code is modular and maintainable. If you have any questions or need further assistance, feel free to ask!

# Refactor the script to OOP

To modify the script to use Object-Oriented Programming (OOP) principles, we can create a class that encapsulates the functionality of the script. Here's an example of how you can do this:

```python
import pandas as pd

class DataProcessor:
    def __init__(self, input_files, rows_to_extract):
        self.input_files = input_files
        self.rows_to_extract = rows_to_extract
        self.df = None
        self.result_df = None

    def parse_csv_files(self):
        extracted_data = []
        for input_file in self.input_files:
            with open(input_file, 'r') as file:
                lines = file.readlines()
            current_block = {}
            for line in lines[4:]:
                if line.strip() == "Sample start":
                    if current_block:
                        extracted_data.append(current_block)
                    current_block = {}
                else:
                    for row in self.rows_to_extract:
                        if line.startswith(row):
                            current_block[row] = line.split(";")[1].strip()
            if current_block:
                extracted_data.append(current_block)
        self.df = pd.DataFrame(extracted_data, columns=self.rows_to_extract)
        for col in self.df.columns[:-1]:
            self.df[col] = pd.to_numeric(self.df[col])
        self.df[self.df.columns[-1]] = pd.to_datetime(self.df[self.df.columns[-1]], format='%d/%m/%Y %H:%M:%S')

    def compute_quantities(self):
        self.df["LTime"] = self.df["Time"] - self.df["DTime"]
        self.df["Counts_"] = self.df["CPM"] * self.df["Time"] / 60
        self.df["UCounts"] = self.df["Counts_"].pow(1/2)
        self.df["UrCounts"] = self.df["UCounts"] / self.df["Counts_"] * 100

    def transform_dataframe(self):
        df_b = self.df[self.df["Samp."] == self.df["Samp."].unique()[0]].reset_index(drop=True)
        df_s = self.df[self.df["Samp."] == self.df["Samp."].unique()[1]].reset_index(drop=True)
        df_b.columns = [col + "_bkgd" for col in df_b.columns]
        df_s.columns = [col + "_smpl" for col in df_s.columns]
        self.result_df = pd.concat([df_b, df_s], axis=1)
        self.result_df = self.result_df.drop(['Samp._bkgd', 'Samp._smpl', 'Repe._smpl'], axis=1)
        self.result_df = self.result_df.rename(columns={'Repe._bkgd': 'Repe.'})

    def compute_net_quantities(self):
        self.result_df["CPM_net"] = self.result_df["CPM_smpl"] - self.result_df["CPM_bkgd"]
        self.result_df["Counts_net"] = self.result_df["Counts__smpl"] - self.result_df["Counts__bkgd"]
        self.result_df["UCounts_net"] = (self.result_df["UCounts_smpl"].pow(2) + self.result_df["UCounts_bkgd"].pow(2)).pow(1/2)
        self.result_df["UrCounts_net"] = self.result_df["UCounts_net"] / self.result_df["Counts_net"] * 100

    def compute_elapsed_time(self, unit):
        initial_time = self.result_df['EndTime_smpl'].min()
        self.result_df['ETime'] = self.result_df['EndTime_smpl'] - initial_time
        label = f'ETime ({unit})'
        time_conversion = {
            'seconds': 1, 'minutes': 1/60, 'hours': 1/3600, 'days': 1/86400,
            'weeks': 1/(86400 * 7), 'months': 1/(86400 * 30.44), 'years': 1/(86400 * 365.25)
        }
        if unit not in time_conversion:
            raise ValueError("Invalid unit. Choose from 'seconds', 'minutes', 'hours', 'days', 'weeks', 'months', or 'years'.")
        elapsed_seconds = pd.Series([i.total_seconds() for i in self.result_df['ETime']]) * time_conversion[unit]
        self.result_df[label] = elapsed_seconds

    def save_results(self):
        self.df.to_csv('output1.csv', index=False)
        self.result_df.to_csv('output2.csv', index=False)
        print("Data extracted, types converted, and saved to output.csv")

def main():
    rows_to_extract = ["Samp.", "Repe.", "CPM", "Counts", "DTime", "Time", "EndTime"]
    input_files = ['csv_type1_1.csv', 'csv_type1_2.csv']
    
    processor = DataProcessor(input_files, rows_to_extract)
    
    # Step 1: Parse CSV files
    processor.parse_csv_files()
    
    # Step 2: Compute quantities for each measurement
    processor.compute_quantities()
    
    # Step 3: Transform the DataFrame based on measurement types
    processor.transform_dataframe()
    
    # Step 4: Compute net quantities
    processor.compute_net_quantities()
    
    # Step 5: Compute elapsed time
    unit = 'minutes'  # Change this to the desired unit
    processor.compute_elapsed_time(unit)
    
    # Save the results
    processor.save_results()

if __name__ == "__main__":
    main()
```

In this version, the `DataProcessor` class encapsulates all the functionality. Each method corresponds to one of the steps in your original script. The `main` function creates an instance of `DataProcessor` and calls the methods in sequence. This approach makes the code more modular and easier to maintain.