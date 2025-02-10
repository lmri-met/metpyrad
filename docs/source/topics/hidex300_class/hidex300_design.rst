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
During this step, the user provides essential information about the radionuclide being measured, as well as the year and month of the measurements.
This setup ensures that the class is configured with the correct context for the data it will process.

During the initialization, the constructor (``__init__``) is called with parameters for the ``radionuclide``, ``year``, and ``month`` of the measurements.
These parameters are stored as the configuration attributes of the class instance (``radionuclide``, ``year``, and ``month``).
Data storage attributes (``readings``, ``background``, ``sample``, ``net``)
and measurement attributes (``cycles``, ``cycle_repetitions``, ``repetition_time``, ``total_measurements``, ``measurement_time``)
are initialized to ``None``.

Parsing readings
----------------

Once the class is initialized, the next step is to parse the measurement data.
The user specifies the folder containing the CSV files with the raw data.
The ``parse_readings`` method reads these files, extracts the relevant information, and organizes it into a structured format.
This parsed data is stored in the ``readings`` attribute, making it ready for further processing.

The ``parse_readings`` method is responsible for reading and parsing measurement data from CSV files located in a specified folder.
This method uses the ``_parse_readings`` private method to handle the actual parsing logic.

- **Steps**:

  - Retrieve a list of CSV files from the specified folder using ``_get_csv_files``.
  - Iterate over each file, reading lines and extracting relevant data based on predefined rows and delimiters.
  - Convert the extracted data into a DataFrame, ensuring consistency in repetitions per cycle.
  - Store the parsed data in the ``readings`` attribute.

- **Key Considerations**:

  - Consistency checks for repetitions per cycle.
  - Conversion of date and time strings to datetime format.
  - Sorting and resetting the index of the DataFrame.

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
