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

# Save the DataFrame to a CSV file
df.to_csv('output.csv', index=False)

print("Data extracted, types converted, and saved to output.csv")
