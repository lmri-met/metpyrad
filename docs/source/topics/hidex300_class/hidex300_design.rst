Workflow of the class
=====================

The workflow of the class involves several key steps, each contributing to the overall process of handling measurement data.
Here is a general description of the workflow:

1. **Initialization**: Set up the class with the necessary information about the radionuclide and the measurement period.
2. **Parsing readings**: Read and organize raw measurement data from CSV files into a structured format.
3. **Processing measurements**: Categorize and process the parsed data into background, sample, and net measurements.
4. **Summarizing data**: Generate a concise overview of the processed data, including key statistics and information.
5. **Exporting results**: Save the processed data and visualizations to CSV and PNG files for further analysis and reporting.
6. **Comprehensive analysis**: Combine all steps into a single workflow for a complete analysis of the measurement data.

Initialization
--------------

The workflow begins with the initialization of the ``Hidex300`` class.
During this step, the user provides information about the radionuclide being measured,
such as the name of the radionuclide, and the year and month of the measurements.
This setup ensures that the class is configured with the correct context for the data it will process.

During the initialization, the constructor (``__init__``) is called with parameters for the ``radionuclide``, ``year``, and ``month`` of the measurements.
These parameters are stored as the configuration attributes of the class instance (``radionuclide``, ``year``, and ``month``).

Data storage attributes (``readings``, ``background``, ``sample``, ``net``)
and measurement attributes (``cycles``, ``cycle_repetitions``, ``repetition_time``, ``total_measurements``, ``measurement_time``)
are initialized to ``None``.

Parsing readings
----------------

Once the class is initialized, the next step is to parse the measurement data.
The user specifies the folder containing the CSV files provided by the Hidex 300 SL automatic counter from the measurement of the radionuclide.

Then, the ``parse_readings`` method orchestrates the parsing of measurement data from CSV files located in this folder.
It reads the CSV files in this folder, extracts the relevant information, and organizes it into a structured format.

Parsing the CSV files
^^^^^^^^^^^^^^^^^^^^^

The ``parse_readings`` method calls the ``_parse_readings`` private method to handle the detailed parsing logic,
which includes reading the files, extracting relevant data, and organizing it into a structured DataFrame.

Getting the CSV files
"""""""""""""""""""""

The ``_parse_readings`` method retrieves a list of relevant CSV files that need to be processed
calling to the ``_get_csv_files`` helper function.
This function iterates over all the files in the given folder, checks if each file has a ``.csv`` extension,
and appends the absolute path of each CSV file to a list.
The method then prints the number of CSV files found and returns the list of full paths to these files.

Identifying information blocks
""""""""""""""""""""""""""""""

Then, the ``_parse_readings`` method iterate over the CSV files.
For each file, it reads the file line by line, and extracts relevant data based on predefined parameters.
These parameters are defined as class private constants.

The method assign to each file an identification number.
The method skips 4 of initial metadata lines (specified by the ``_ID_LINES`` class constant).
It identifies the start of new data blocks by the key ``Sample start``
(defined in the ``_BLOCK_STARTER`` class constant).

Extracting block information
""""""""""""""""""""""""""""

Then, for each new data block, the ``_parse_readings`` method extracts the values in the rows that starts with
``Samp.``, ``Repe.``, ``CPM``, ``Counts``, ``DTime``, ``Time`` or ``EndTime``.
These keys are defined in the ``_ROWS_TO_EXTRACT`` class constant.

These values represent respectively the type of sample (background or radionuclide sample), the number of the repetition,
the count rate, the total counts, the dead time, the measurement time and the end time of the measurement.
The delimiter to use when parsing the values is ``;``, defined in the ``_DELIMITER`` class constant.

The method compiles the extracted information for each block into a dictionary, adding also the file identification number.
Then, it compiles the extracted information for all blocks into a list.

Structuring the data
""""""""""""""""""""

Then, ``_parse_readings`` method structures all the extracted data in a DataFrame,
being the columns the key words defined in the ``_ROWS_TO_EXTRACT`` class constant,
and each row corresponding to a single measurement of background or radionuclide sample.

Then, it converts the strings of all the columns to numeric format, except for the ``EndTime`` column.
It converts date and time strings of the ``EndTime`` column to ``datetime`` objects
using the format ``%d/%m/%Y %H:%M:%S`` (specified in the ``_DATE_TIME_FORMAT`` class constant).

Then, it sorts the DataFrame by end time of the measurements,
and reassign the file identification number to match the chronological order of the measurements.
It ensures consistency in repetitions per cycle. If not it will raise a ``ValueError``.

Assigning attributes
""""""""""""""""""""

Finally, the ``_parse_readings`` method renames columns for clarity and returns the structured DataFrame.
The ``parse_readings`` method assign this DataFrame to the ``readings`` class attribute.

Getting readings statistics
^^^^^^^^^^^^^^^^^^^^^^^^^^^

After parsing the readings to a structured DataFrame, the ``parse_readings`` method generates
a summary of the measurement cycles and their key attributes using the ``_get_readings_statistics`` private method.

Summary of measurement cycles
"""""""""""""""""""""""""""""

The ``_get_readings_statistics`` starts generating a summary of the measurement cycles and their key attributes
using the ``_get_readings_summary`` private method.

The ``_get_readings_summary`` iterates over each unique cycle in the readings DataFrame, stored in the ``readings`` class attribute.
For each cycle, it filters the DataFrame, determines the number of repetitions per cycle,
retrieves the real time of measurement for the repetitions, and identifies the earliest end time of the measurements.

It compiles these details into a list of results, which is then converted into a summary DataFrame
containing the cycle, repetitions per cycle, real time of the measurement, and the date and time of the measurement cycle.

If the real time values are not consistent for all measurements, it will raise a ``ValueError``.
If the ``readings`` class attribute is ``None``, it will raise a ``ValueError``,
indicating that the readings must be parsed first from the CSV files.

Summary of all measurements
"""""""""""""""""""""""""""

After getting the measurement cycles summary DataFrame, the ``_get_readings_statistics`` method
checks for consistency in repetitions per cycle. If they are not consistent, it will raise a ``ValueError``.

Then, from this Dataframe, it calculates the number of cycles, the total number of measurements, the total measurement time,
the time per repetition, and the number of repetitions per cycle.
These statistics are compiled into a dictionary and returned.

Finally, the ``parse_readings`` method assigns these statistics to the corresponding measurement attributes of the class.

Processing measurements
-----------------------

With the raw data parsed, the class proceeds to process the measurements.
This involves categorizing the data into different types: background measurements, sample measurements, and net measurements.
The ``process_readings`` method handles this task, ensuring that each type of measurement is correctly identified and processed.
The processed data is then stored in the respective attributes (``background``, ``sample``, ``net``),
providing a clear separation of the different measurement types.

The ``process_readings`` method processes the parsed data to generate background, sample, and net measurements. It calls specific private methods based on the type of measurements to be processed.

- **Steps**:

  - For background measurements, call ``_get_background_sample`` with ``kind='background'``.
  - For sample measurements, call ``_get_background_sample`` with ``kind='sample'``.
  - For net measurements, call ``_get_net_measurements``.
  - For all measurements, process background, sample, and net sequentially.

- **Key Considerations**:

  - Calculation of elapsed time and live time.
  - Handling of different time units (seconds, minutes, hours, etc.).
  - Calculation of counts and counts uncertainty.

Summarizing data
----------------

After processing the measurements, the class generates a summary of the data.
The ``summarize_readings`` method compiles key statistics and information, offering a concise overview of the measurements.
This summary can be printed directly for immediate review or saved to a text file for future reference.
The summary includes details such as the number of cycles, repetitions per cycle, total measurement time, and other relevant metrics.

The ``summarize_readings`` method generates a summary of the processed data. It can print the summary directly or save it to a text file.

- **Steps**:

  - Generate a summary string using the ``__str__`` method, which compiles key statistics and information.
  - If ``save=True``, write the summary to a text file in the specified folder.

- **Key Considerations**:

  - Inclusion of detailed summary information if all relevant attributes are not ``None``.
  - Handling of file operations for saving the summary.

Exporting results
-----------------

To facilitate further analysis and reporting, the class provides methods for exporting the processed data and visualizations.
Users can export the data tables to CSV files using the ``export_table`` method, making it easy to share and analyze the data in other applications.
Additionally, the ``export_plot`` method allows users to save visual representations of the measurements as PNG files, providing a graphical overview of the data.

The class provides methods for exporting the processed data and visualizations to CSV and PNG files.

- **Export Tables**:

  - The ``export_table`` method exports specified types of measurements to CSV files.
  - It uses a dictionary to map measurement kinds to their corresponding DataFrames.
  - The DataFrame is then saved to a CSV file in the specified folder.

- **Export Plots**:

  - The ``export_plot`` method exports specified types of measurement plots to PNG files.
  - It calls the ``plot_measurements`` method to generate the plots and then saves them using ``plt.savefig``.

- **Key Considerations**:

  - Validation of measurement kinds.
  - Handling of file operations for saving CSV and PNG files.

Comprehensive analysis
----------------------

For users seeking a complete analysis workflow, the ``analyze_readings`` method combines all the previous steps into a single, streamlined process.
This method handles the parsing, processing, summarizing, and exporting of the data in one go.
Users simply provide the input folder containing the raw data and specify whether they want to save the results.
The method then executes the entire workflow, producing a comprehensive analysis of the measurement data.

The ``analyze_readings`` method combines parsing, processing, summarizing, and exporting into a single workflow for comprehensive analysis.

- **Steps**:

  - Parse readings from the input folder.
  - Process all types of measurements.
  - Print the summary of the measurements.
  - If ``save=True``, save the results to the specified output folder, including CSV files and plots.

- **Key Considerations**:

  - Ensuring the output folder exists or creating it if necessary.
  - Handling of file operations for saving all results.
  - Comprehensive error handling to manage potential issues during the workflow.
