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

# Transforming the extracted data
## Goal
The goal of this script is to transform a DataFrame by splitting it based on a column value, renaming columns for distinction, and concatenating the results side by side for easy comparison.

The initial DataFrame has the following structure:

1. **Columns**:
   - `Samp.`: Sample number
   - `Repe.`: Repeat number
   - `CPM`: Counts per minute
   - `Counts`: Total counts
   - `DTime`: Dwell time
   - `Time`: Measurement time
   - `EndTime`: End time of the measurement

2. **Rows**:
   - Each row represents a specific measurement with values for the columns listed above.

### Example of the Initial DataFrame:
```
   Samp.  Repe.        CPM  Counts  DTime  Time             EndTime
0      1      1     97.770     163  1.000   100  01/12/2023 12:46:16
1      1      2     85.170     142  1.000   100  01/12/2023 12:53:00
2      2      1  223744.100  335987  1.110   100  01/12/2023 12:49:40
3      2      2  223689.400  335843  1.110   100  01/12/2023 12:56:24
4      1      1     95.360     159  1.000   100  02/12/2023 17:57:24
5      1      2     98.360     164  1.000   100  02/12/2023 18:04:08
6      2      1  196139.010  298162  1.096   100  02/12/2023 18:00:48
7      2      2  197290.350  299733  1.097   100  02/12/2023 18:07:32
```

This DataFrame contains measurements for different samples (`Samp.`) and repeats (`Repe.`), along with their corresponding values for `CPM`, `Counts`, `DTime`, `Time`, and `EndTime`.

The final DataFrame has the following structure:

1. **Columns**:
   - The columns are divided into two sets, each corresponding to the original data blocks but with distinct suffixes (`_B` for the first set and `_S` for the second set):
     - `Samp._B`, `Repe._B`, `CPM_B`, `Counts_B`, `DTime_B`, `Time_B`, `EndTime_B`
     - `Samp._S`, `Repe._S`, `CPM_S`, `Counts_S`, `DTime_S`, `Time_S`, `EndTime_S`

2. **Rows**:
   - Each row represents a pair of corresponding measurements from the two original data blocks, aligned side by side for easy comparison.

### Example of the Final DataFrame:
```
   Samp._B  Repe._B      CPM_B  Counts_B  DTime_B  Time_B           EndTime_B  Samp._S  Repe._S       CPM_S  Counts_S  DTime_S  Time_S           EndTime_S
0        1        1     97.770       163    1.000     100  01/12/2023 12:46:16        2        1  223744.100    335987    1.110     100  01/12/2023 12:49:40
1        1        2     85.170       142    1.000     100  01/12/2023 12:53:00        2        2  223689.400    335843    1.110     100  01/12/2023 12:56:24
2        1        1     95.360       159    1.000     100  02/12/2023 17:57:24        2        1  196139.010    298162    1.096     100  02/12/2023 18:00:48
3        1        2     98.360       164    1.000     100  02/12/2023 18:04:08        2        2  197290.350    299733    1.097     100  02/12/2023 18:07:32
```

In this example:
- The first set of columns (`_B`) contains the data from the first sample block.
- The second set of columns (`_S`) contains the data from the second sample block.
- Each row pairs corresponding measurements from the two blocks, making it easy to compare the data side by side.

This structured format facilitates easy comparison and analysis of the data from the two original blocks.
## Script
To transform your DataFrame as described, you can follow these steps:

1. Split the DataFrame into two separate DataFrames based on the Samp. column.
2. Rename the columns of each DataFrame to distinguish between the two sets of data.
3. Concatenate the two DataFrames side by side.

Here's the code to achieve this:
```python
import pandas as pd

# Create the initial DataFrame
data = {
    "Samp.": [1, 1, 2, 2, 1, 1, 2, 2],
    "Repe.": [1, 2, 1, 2, 1, 2, 1, 2],
    "CPM": [97.770, 85.170, 223744.100, 223689.400, 95.360, 98.360, 196139.010, 197290.350],
    "Counts": [163, 142, 335987, 335843, 159, 164, 298162, 299733],
    "DTime": [1.000, 1.000, 1.110, 1.110, 1.000, 1.000, 1.096, 1.097],
    "Time": [100, 100, 100, 100, 100, 100, 100, 100],
    "EndTime": ["01/12/2023 12:46:16", "01/12/2023 12:53:00", "01/12/2023 12:49:40", "01/12/2023 12:56:24", 
                "02/12/2023 17:57:24", "02/12/2023 18:04:08", "02/12/2023 18:00:48", "02/12/2023 18:07:32"]
}

df = pd.DataFrame(data)

# Split the DataFrame into two DataFrames based on Samp.
df_B = df[df["Samp."] == df["Samp."].unique()[0]].reset_index(drop=True)
df_S = df[df["Samp."] == df["Samp."].unique()[1]].reset_index(drop=True)

# Rename columns for each DataFrame
df_B.columns = [col + "_B" for col in df_B.columns]
df_S.columns = [col + "_S" for col in df_S.columns]

# Concatenate the two DataFrames side by side
result_df = pd.concat([df_B, df_S], axis=1)

print(result_df)
```
Explanation:
1. **Create the initial DataFrame**: This step sets up your initial DataFrame with the given data.
2. **Split the DataFrame**: The DataFrame is split into two based on the unique values in the Samp. column.
3. **Rename columns**: Columns in each DataFrame are renamed to distinguish between the two sets of data (_B for the first set and _S for the second set).
4. **Concatenate DataFrames**: The two DataFrames are concatenated side by side to form the final DataFrame. 
 
This will give you the desired output DataFrame. If you have any questions or need further assistance, feel free to ask!

# Computing the elapsed time

I have a dataframe in which a column are datetime object. I need to compute in a new column the elapsed time for each row, being the initial time the row with the earliest datetime

You can compute the elapsed time for each row in a DataFrame with a datetime column by following these steps:

1. Convert the datetime column to datetime objects (if not already done).
2. Find the earliest datetime in the column.
3. Compute the elapsed time for each row by subtracting the earliest datetime from each datetime value in the column.
4. Store the result in a new column.

Here's an example of how to do this:
```python
import pandas as pd

# Sample DataFrame with a datetime column
data = {
    'Event': ['A', 'B', 'C', 'D'],
    'DateTime': ['2023-01-01 12:00:00', '2023-01-01 14:30:00', '2023-01-01 16:45:00', '2023-01-02 09:15:00']
}
df = pd.DataFrame(data)

# Convert the DateTime column to datetime objects
df['DateTime'] = pd.to_datetime(df['DateTime'])

# Find the earliest datetime
initial_time = df['DateTime'].min()

# Compute the elapsed time for each row
df['ElapsedTime'] = df['DateTime'] - initial_time

print(df)
```
Explanation:
1. Convert the DateTime column to datetime objects:
   ```python
   df['DateTime'] = pd.to_datetime(df['DateTime'])
   ```
   This ensures that the DateTime column is in the correct datetime format.

2. Find the earliest datetime:
   ```python
   initial_time = df['DateTime'].min()
   ```
   This finds the earliest datetime in the DateTime column.

3. Compute the elapsed time for each row:
   ```python
   df['ElapsedTime'] = df['DateTime'] - initial_time
   ```
   This calculates the elapsed time for each row by subtracting the earliest datetime from each datetime value in the column.

Example Output:
```
  Event            DateTime        ElapsedTime
0     A 2023-01-01 12:00:00  0 days 00:00:00
1     B 2023-01-01 14:30:00  0 days 02:30:00
2     C 2023-01-01 16:45:00  0 days 04:45:00
3     D 2023-01-02 09:15:00  0 days 21:15:00
```
In this example, the ElapsedTime column shows the time difference between each row's datetime and the earliest datetime in the DataFrame.

If you have any questions or need further assistance, feel free to ask!

## Specific datetime format

When converting types of a dataframe column using:
df[df.columns[-1]] = pd.to_datetime(df[df.columns[-1]])
The strings in this column have the format:
 day/month/year hour:min
How to transform this correctly to a datetime object?

To correctly transform strings in the format `day/month/year hour:min` to datetime objects, you can use the `pd.to_datetime` function with the `format` parameter. This parameter allows you to specify the exact format of the datetime strings.

Here's how you can do it:

```python
import pandas as pd

# Sample DataFrame with a datetime column in the format day/month/year hour:min
data = {
    'Event': ['A', 'B', 'C', 'D'],
    'DateTime': ['01/12/2023 12:46', '01/12/2023 14:30', '01/12/2023 16:45', '02/12/2023 09:15']
}
df = pd.DataFrame(data)

# Convert the DateTime column to datetime objects with the specified format
df['DateTime'] = pd.to_datetime(df['DateTime'], format='%d/%m/%Y %H:%M')

print(df)
```

### Explanation:
- **`format='%d/%m/%Y %H:%M'`**:
  - `%d`: Day of the month as a zero-padded decimal number (01-31).
  - `%m`: Month as a zero-padded decimal number (01-12).
  - `%Y`: Year with century as a decimal number.
  - `%H`: Hour (24-hour clock) as a zero-padded decimal number (00-23).
  - `%M`: Minute as a zero-padded decimal number (00-59).

This ensures that the `DateTime` column is correctly parsed according to the specified format.

### Example Output:
```
  Event            DateTime
0     A 2023-12-01 12:46:00
1     B 2023-12-01 14:30:00
2     C 2023-12-01 16:45:00
3     D 2023-12-02 09:15:00
```

This will correctly convert the strings in the `DateTime` column to datetime objects. If you have any questions or need further assistance, feel free to ask!

## Custom elapsed time column

This code snippet calculates the elapsed time between measurements in a DataFrame and converts it into a specific unit (e.g., minutes, hours, days). Here's a step-by-step explanation:

1. **Find the earliest datetime**:
    ```python
    initial_time = result_df['EndTime_smpl'].min()
    ```
    This line finds the earliest datetime in the `EndTime_smpl` column of the `result_df` DataFrame.

2. **Compute the elapsed time for each row**:
    ```python
    result_df['ETime'] = result_df['EndTime_smpl'] - initial_time
    ```
    This line calculates the elapsed time for each row by subtracting the earliest datetime (`initial_time`) from each datetime value in the `EndTime_smpl` column. The result is stored in a new column called `ETime`.

3. **Specify the unit for elapsed time**:
    ```python
    unit = 'minutes'
    label = f'ETime ({unit})'
    ```
    These lines set the desired unit for the elapsed time calculation (in this case, 'minutes') and create a label for the new column that will store the converted elapsed time.

4. **Define time conversion factors**:
    ```python
    time_conversion = {'seconds':1, 'minutes':1/60, 'hours':1/3600,'days':1/ 86400,'weeks':1/ (86400 * 7),'months':1/ (86400 * 30.44),'years':1/ (86400 * 365.25)}
    ```
    This dictionary contains conversion factors to convert elapsed time from seconds to the desired unit.

5. **Validate the unit**:
    ```python
    if unit not in time_conversion:
        raise ValueError("Invalid unit. Choose from 'seconds', 'minutes', 'hours', or 'days'.")
    ```
    This block checks if the specified unit is valid. If not, it raises a `ValueError`.

6. **Convert elapsed time to the specified unit**:
    ```python
    elapsed_seconds = pd.Series([i.total_seconds() for i in result_df['ETime']])*time_conversion[unit]
    result_df[label] = elapsed_seconds
    ```
    - This line converts the `ETime` values to total seconds using the `total_seconds()` method.
    - It then multiplies the total seconds by the appropriate conversion factor from the `time_conversion` dictionary to get the elapsed time in the specified unit.
    - The result is stored in a new column with the label `ETime (minutes)`.

In summary, this code calculates the elapsed time between measurements in a DataFrame, converts it to a specified unit, and adds the result as a new column in the DataFrame.

Example output Dataframe:
```
  Event          EndTime_smpl            ETime  ETime (minutes)
0     A 2023-12-01 12:46:16 0 days 00:00:00     0.000000
1     B 2023-12-01 14:30:45 0 days 01:44:29   104.483333
2     C 2023-12-01 16:45:30 0 days 03:59:14   239.233333
3     D 2023-12-02 09:15:10 0 days 20:28:54  1228.900000
```