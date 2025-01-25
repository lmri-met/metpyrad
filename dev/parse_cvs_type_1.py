# The goal of this script is to process multiple CSV files, extract specific data, compute various quantities, transform the data based on measurement types, calculate net quantities, determine elapsed time in user-specified units, and save the results to new CSV files.
# This script performs several tasks to process and analyze data from multiple CSV files. Here's a detailed description of what it does:
# 1. Parse Type1 CSV Files:
# - Reads multiple CSV files (csv_type1_1.csv, csv_type1_2.csv).
# - Extracts specific rows (e.g., Samp., Repe., CPM, Counts, DTime, Time, EndTime) from each block of data within the files.
# - Stores the extracted data in a DataFrame.
# - Converts the extracted columns to numeric types, except for the last column, which is converted to datetime objects.
# 2.Compute Quantities for Each Measurement:
# - Computes the live time (LTime) as the difference between Time and DTime.
# - Calculates total counts (Counts_) as the product of CPM and Time, divided by 60.
# - Computes the uncertainty of total counts (UCounts) as the square root of Counts_.
# - Calculates the relative uncertainty of total counts (UrCounts) as the ratio of UCounts to Counts_, multiplied by 100.
# 3. Transform the DataFrame Based on Background or Sample Measurements:
# - Splits the DataFrame into two separate DataFrames based on the Samp. column (background and sample measurements).
# - Renames the columns of each DataFrame to distinguish between background (_bkgd) and sample (_smpl) measurements.
# - Concatenates the two DataFrames side by side.
# - Drops unnecessary columns (Samp._bkgd, Samp._smpl, Repe._smpl) and renames the repetition column (Repe._bkgd to Repe.).
# 4. Compute Net Quantities:
# - Calculates the net count rate (CPM_net) as the difference between sample and background count rates.
# - Computes net counts (Counts_net) as the difference between sample and background counts.
# - Calculates the uncertainty of net counts (UCounts_net) as the square root of the sum of the squares of sample and background uncertainties.
# - Computes the relative uncertainty of net counts (UrCounts_net) as the ratio of UCounts_net to Counts_net, multiplied by 100.
# 5. Find the Elapsed Time Between Measurements:
# - Finds the earliest datetime in the EndTime_smpl column.
# - Computes the elapsed time for each row as the difference between each datetime and the earliest datetime.
# - Converts the elapsed time to a user-specified unit (e.g., minutes) and adds it as a new column.
# 6. Save the Results:
# - Saves the initial DataFrame to output1.csv.
# - Saves the transformed and computed results to output2.csv.
# In summary, this script processes CSV files to extract and compute various data points, transforms the data for analysis, calculates net quantities, determines elapsed time, and saves the results to new CSV files.
import pandas as pd

# STEP 1: Parse type1 CSV files to a dataframe

# Define the rows to extract
rows_to_extract = ["Samp.", "Repe.", "CPM", "Counts", "DTime", "Time", "EndTime"]

# Initialize an empty list to store the extracted data
extracted_data = []

# List of input CSV files
input_files = ['csv_type1_1.csv', 'csv_type1_2.csv']

# Process each input file
for input_file in input_files:
    # Read the CSV file
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Process the file to extract the required rows from each block
    current_block = {}
    for line in lines[4:]:  # Skip the first 4 rows
        if line.strip() == "Sample start":
            if current_block:
                extracted_data.append(current_block)
            current_block = {}
        else:
            for row in rows_to_extract:
                if line.startswith(row):
                    current_block[row] = line.split(";")[1].strip()

    # Append the last block if it exists
    if current_block:
        extracted_data.append(current_block)

# Create a DataFrame from the extracted data
df = pd.DataFrame(extracted_data, columns=rows_to_extract)

# Convert columns to numeric, except the last one which should be a date object
for col in df.columns[:-1]:
    df[col] = pd.to_numeric(df[col])

df[df.columns[-1]] = pd.to_datetime(df[df.columns[-1]], format='%d/%m/%Y %H:%M:%S')

# STEP 2: Compute quantities for each measurement

# Compute live time
df["LTime"]=df["Time"]-df["DTime"]
# Compute total counts: rate count (1/min) * real time (s) / 60 (s/min)
df["Counts_"]=df["CPM"]*df["Time"]/60
# Compute uncertainty of total counts
df["UCounts"]=df["Counts_"].pow(1/2)
# Compute relative uncertainty of total counts
df["UrCounts"]=df["UCounts"]/df["Counts_"]*100

# STEP 3: Transform the DataFrame based of background or sample measurements

# Split the DataFrame into two DataFrames based on Samp.
df_b = df[df["Samp."] == df["Samp."].unique()[0]].reset_index(drop=True)
df_s = df[df["Samp."] == df["Samp."].unique()[1]].reset_index(drop=True)

# Rename columns for each DataFrame
df_b.columns = [col + "_bkgd" for col in df_b.columns]
df_s.columns = [col + "_smpl" for col in df_s.columns]

# Concatenate the two DataFrames side by side
result_df = pd.concat([df_b, df_s], axis=1)

# Drop sample coumns for background and sample and repetition column for sample
result_df = result_df.drop(['Samp._bkgd', 'Samp._smpl', 'Repe._smpl'], axis=1)

# Rename repetition column
result_df = result_df.rename(columns={'Repe._bkgd': 'Repe.'})

# STEP 4: Compute net quantities

# Compute net count rate: sample count rate - background count rate
result_df["CPM_net"]=result_df["CPM_smpl"]-result_df["CPM_bkgd"]
# Compute net counts: sample counts - background counts
result_df["Counts_net"]=result_df["Counts__smpl"]-result_df["Counts__bkgd"]
# Compute uncertainty of net counts
result_df["UCounts_net"]=(result_df["UCounts_smpl"].pow(2)+result_df["UCounts_bkgd"].pow(2)).pow(1/2)
# Compute relative uncertainty of net counts
result_df["UrCounts_net"]=result_df["UCounts_net"]/result_df["Counts_net"]*100

# STEP 5: Find the elapsed time between measurements

# Find the earliest datetime
initial_time = result_df['EndTime_smpl'].min()

# Compute the elapsed time for each row
result_df['ETime'] = result_df['EndTime_smpl'] - initial_time

# Compute the elapsed time for each row in a specific unit
unit = 'minutes'
label = f'ETime ({unit})'
time_conversion = {'seconds':1, 'minutes':1/60, 'hours':1/3600,'days':1/ 86400,'weeks':1/ (86400 * 7),'months':1/ (86400 * 30.44),'years':1/ (86400 * 365.25)}
if unit not in time_conversion:
    raise ValueError("Invalid unit. Choose from 'seconds', 'minutes', 'hours', or 'days'.")
elapsed_seconds = pd.Series([i.total_seconds() for i in result_df['ETime']])*time_conversion[unit]
result_df[label] = elapsed_seconds

# STEP: Save the results

# Save the DataFrame to a CSV file
df.to_csv('output1.csv', index=False)
result_df.to_csv('output2.csv', index=False)

print("Data extracted, types converted, and saved to output.csv")
