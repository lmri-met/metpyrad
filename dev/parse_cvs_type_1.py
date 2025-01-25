import pandas as pd

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
    df[col] = pd.to_numeric(df[col], errors='coerce')

df[df.columns[-1]] = pd.to_datetime(df[df.columns[-1]], errors='coerce')

# Compute live time
df["LTime"]=df["Time"]-df["DTime"]
# Compute total counts: rate count (1/min) * real time (s) / 60 (s/min)
df["Counts_"]=df["CPM"]*df["Time"]/60
# Compute uncertainty of total counts
df["UCounts"]=df["Counts_"].pow(1/2)
# Compute relative uncertainty of total counts
df["UrCounts"]=df["UCounts"]/df["Counts_"]*100

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

# Save the DataFrame to a CSV file
df.to_csv('output1.csv', index=False)
result_df.to_csv('output2.csv', index=False)

print("Data extracted, types converted, and saved to output.csv")
