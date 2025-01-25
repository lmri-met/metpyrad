# Script to parse data from CSV file type 1

## Goal
The purpose of this script is to extract specific data from blocks within a CSV file and organize it into a structured format. It reads the CSV file, skips initial identification rows, processes each data block, extracts values for specified identifiers, and saves the organized data into a new CSV file. This makes it easier to analyze and work with the extracted information.
## How is the CSV input file?
The input CSV file has the following structure:

1. **Identification Information** (Rows 1-4):
   - These rows contain metadata about the file, such as the name, start time, and other descriptive details.

2. **Data Blocks**:
   - Each block starts with the line "Sample start".
   - Each block contains rows with various data points, including:
     - `Samp.`: Sample number
     - `Repe.`: Repeat number
     - `CPM`: Counts per minute
     - `Counts`: Total counts
     - `DTime`: Dwell time
     - `Time`: Measurement time
     - `EndTime`: End time of the measurement
   - The number of blocks can vary between files.

3. **Delimiter**:
   - The delimiter used in the file is a semicolon (`;`).

Here's an example of the input CSV file structure:

```
Lu-177 HS3 011223_ciclo1
Start Time 12:42:53
- ROI1 Free Channel Limits 1 - 1023, Type Beta
Counting type: Low
Sample start
Samp.;1
Repe.;1
Vial;1
WName;A01
CPM;97.770
Counts;163
DTime;1.000
Time;100
EndTime;01/12/2023 12:46:16
...
Sample start
Samp.;2
Repe.;1
Vial;8
WName;A08
CPM;223744.100
Counts;335987
DTime;1.110
Time;100
EndTime;01/12/2023 12:49:40
...
```

Each block contains the data points for a specific sample, and the script extracts these points to create a structured output.
## How is the CSV output file?
The output CSV file has a structured format with the following characteristics:

1. **Column Labels**:
   - The first row contains the column labels: `Samp.`, `Repe.`, `CPM`, `Counts`, `DTime`, `Time`, `EndTime`.

2. **Data Rows**:
   - Each subsequent row contains the extracted values for each block from the input CSV file.
   - Each row represents a single block, with values corresponding to the specified identifiers.

Here's an example of what the output CSV file might look like:

```
Samp.,Repe.,CPM,Counts,DTime,Time,EndTime
1,1,97.770,163,1.000,100,01/12/2023 12:46:16
2,1,223744.100,335987,1.110,100,01/12/2023 12:49:40
```

In this example:
- The first row contains the column labels.
- Each subsequent row contains the data extracted from each block in the input CSV file, organized under the appropriate columns. 

This structured format makes it easy to analyze and work with the extracted data.
# Script description
Absolutely! Let's break down the code step by step:

1. **Importing the pandas library**:
    ```python
    import pandas as pd
    ```
    This line imports the pandas library, which is used for data manipulation and analysis.

2. **Defining the rows to extract**:
    ```python
    rows_to_extract = ["Samp.", "Repe.", "CPM", "Counts", "DTime", "Time", "EndTime"]
    ```
    Here, we define a list of the row identifiers that we want to extract from each block in the CSV file.

3. **Initializing an empty list to store the extracted data**:
    ```python
    extracted_data = []
    ```
    This list will hold the data extracted from each block.

4. **Reading the CSV file**:
    ```python
    with open('csv_type1.csv', 'r') as file:
        lines = file.readlines()
    ```
    This block of code opens the CSV file named `input.csv` and reads all its lines into a list called `lines`.

5. **Processing the file to extract the required rows from each block**:
    ```python
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
    ```
    - We initialize an empty dictionary `current_block` to store the data for the current block.
    - We loop through the lines starting from the 5th line (index 4) to skip the identification information.
    - If a line contains "Sample start", it indicates the beginning of a new block. If `current_block` is not empty, we append it to `extracted_data` and reset `current_block`.
    - For each line, we check if it starts with any of the identifiers in `rows_to_extract`. If it does, we split the line by the semicolon (`;`) and store the second part (the value) in `current_block`.

6. **Appending the last block if it exists**:
    ```python
    if current_block:
        extracted_data.append(current_block)
    ```
    After the loop, we check if `current_block` contains any data and append it to `extracted_data`.

7. **Creating a DataFrame from the extracted data**:
    ```python
    df = pd.DataFrame(extracted_data, columns=rows_to_extract)
    ```
    We create a pandas DataFrame from `extracted_data` with the specified column labels.

8. **Saving the DataFrame to a CSV file**:
    ```python
    df.to_csv('output.csv', index=False)
    ```
    This line saves the DataFrame to a new CSV file named `output.csv` without including the index.

9. **Printing a confirmation message**:
    ```python
    print("Data extracted and saved to output.csv")
    ```
    Finally, we print a message to confirm that the data has been successfully extracted and saved.

Feel free to ask if you have any questions or need further clarification on any part of the code!