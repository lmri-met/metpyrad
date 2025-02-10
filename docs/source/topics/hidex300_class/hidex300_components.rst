Key components of the class
===========================

The ``Hidex300`` class is composed of several types of components, each serving a specific purpose in the overall functionality of the class.
These components include attributes, constants, public methods, private methods, and helper functions.
Here's a general description of each type.

Attributes
----------

Attributes in the ``Hidex300`` class are used to store information about the measurements and their processing state.
They provide a way to maintain the state of the class and make the data accessible for various operations.
All attributes are public.

These are the attributes in the ``Hidex300`` class:

1. **Configuration attributes**: These attributes identify the measurement of the radionuclide:

   - **radionuclide**: Stores the name of the radionuclide being measured.
   - **year**: Stores the year of the measurements.
   - **month**: Stores the month of the measurements.

2. **Data storage attributes**: These attributes hold the parsed and processed data of the measurements:

   - **readings**: This attribute stores raw measurement data parsed readings from the CSV files in a DataFrame.
   - **background**: This attribute stores the processed background measurements in a DataFrame.
   - **sample**: This attribute stores the processed sample measurements in a DataFrame.
   - **net**: This attribute stores the processed net measurements, which represents the sample measurements after background subtraction, in a DataFrame.

3. **Measurement attributes**: These attributes store information that helps in understanding the repetition structure

   - **cycles**: Stores the number of cycles in the measurements.
   - **cycle_repetitions**: Stores the number of repetitions per cycle.
   - **repetition_time**: Stores the time per repetition in seconds.
   - **total_measurements**: Stores the total number of measurements.
   - **measurement_time**: Stores the total measurement time in seconds.

Public methods
--------------

Public methods in the ``Hidex300`` class are designed to interact with the user and provide the primary interface for using the class.
These methods include functionalities for initializing the class, parsing readings from CSV files,
processing different types of measurements, summarizing the data, and visualizing and exporting results.
Public methods are the main tools that users will call to perform tasks and obtain results from the class.

These are the public methods in the ``Hidex300`` class:

1. **Data processing methods**:

   - **parse_readings**: Parses readings from CSV files in a specified folder.
     This method reads and organizes raw data into the ``readings`` attribute.
     It also updates the measurement attributes.
     It is supported by the ``_parse_readings`` and ``_get_readings_statistics`` private methods.
   - **process_readings**: Processes specified types of measurements (background, sample, net, or all).
     This method generates processed data and from the data stored in the ``readings`` attribute,
     and stores it in the respective attributes (``background``, ``sample`` or ``net``).
     It is supported by the ``_get_background_sample`` and ``_get_net_measurements`` private methods.

2. **Summary methods**:

   - **summarize_readings**: Summarizes the readings and optionally saves the summary to a text file.
     This method provides an overview of the processed data and of the class's state.
     It is supported by the ``__str__`` dunder method.

3. **Plotting methods**:

   - **plot_measurements**: Plots the specified type of measurements (background, sample, or net).
     This method generates visual representations of the data for analysis.
     It is supported by the ``_plot_background_sample_measurements`` and ``_plot_net_measurements`` helper functions.
     It gathers the information from the respective attributes (``background``, ``sample`` or ``net``).

4. **Export methods**:

   - **export_table**: Exports specified types of measurements to CSV files (background, sample, net, or all) to the specified folder.
     This method allows users to save the processed data in a structured format.
     It is supported by the ``_compile_measurements`` private method.
     It gathers the information from the data storage attributes attributes.
   - **export_plot**: Exports specified types of measurement plots to PNG files (background, sample or net) to the specified folder.
     This method provides visual representations of the data.
     It is supported by the ``plot_measurements`` public method.
     It gathers the information from the respective attributes (``background``, ``sample`` or ``net``).

5. **Comprehensive analysis method**:

   - **analyze_readings**: Combines parsing, processing, summarizing, and exporting into a single workflow.
     This method streamlines the entire data processing workflow for comprehensive analysis.
     It gathers the information from the class attributes and it is supported by the class public methods.

Constants
---------

The ``Hidex300`` class includes several private constants that are used to define specific parameters and configurations
for processing measurement data from Hidex 300 SL output CSV files.
These constants help standardize the data parsing and processing operations, ensuring consistency and accuracy.
These constants are not intended to be called directly by the user but are essential for the internal workings of the class.

These are the private constants in the ``Hidex300`` class:

1. **_ROWS_TO_EXTRACT**:
   Specifies the rows to extract from the CSV files.
   It defines the specific labels that identify rows of interest in the CSV files,
   such as sample number, repetitions, count rate, counts, dead time, real time, and end time.

2. **_DATE_TIME_FORMAT**:
   Defines the format for parsing date and time strings from the CSV files.
   It ensures that date and time strings are correctly interpreted and converted to datetime objects during data parsing.

3. **_BLOCK_STARTER**:
   Indicates the string that marks the start of a data block in the CSV files.
   It helps identify the beginning of a new set of measurements within the CSV files, facilitating accurate data extraction.

4. **_ID_LINES**:
   Specifies the number of initial lines to skip from the CSV files.
   It helps to skip header lines that are not relevant to the measurement data.

5. **_DELIMITER**:
   Defines the delimiter used in the CSV files.
   It ensures that the CSV files are correctly parsed by specifying the character that separates values in the files.

6. **_BACKGROUND_ID**:
   Identifier for background measurements in the CSV files.
   It allows to differentiate background measurements from sample measurements, allowing for specific processing of background data.

7. **_SAMPLE_ID**:
   Identifier for sample measurements in the CSV files.
   It allows to differentiate sample measurements from background measurements, allowing for specific processing of sample data.

Private Methods
---------------

Private methods in the ``Hidex300`` class provide internal functionalities that support the operations of the public methods.
They handle specific tasks such as parsing the raw data, calculating statistics, generating summaries, and plotting measurements.
These methods are not intended to be called directly by the user but are essential for the internal workings of the class.
They help to modularize the code and keep the public methods clean and focused on user interactions.

These are the private methods in the ``Hidex300`` class:

1. **Initialization methods**:

   - **__init__**: Initializes the class with the specified radionuclide, year, and month.
     This method sets up the initial configuration of the class.
     These parameters are stored as the configuration attributes of the class instance.
     Data storage attributes and measurement attributes are initialized to ``None``

1. **Data parsing methods**:

   - **_parse_readings**: Parses readings from CSV files in a specified folder and returns a DataFrame.
     This method handles the detailed logic of reading and organizing raw data.
     It is supported by the class constants
     ``_ID_LINES``, ``_BLOCK_STARTER``, ``_DELIMITER``, ``_ROWS_TO_EXTRACT`` and ``_DATE_TIME_FORMAT``.
     It supports the ``parse_readings`` public method.

2. **Data processing methods**:

   - **_get_background_sample**: Processes background or sample measurements and returns them as a DataFrame.
     This method handles the specific processing logic for background and sample data.
     It gathers the information from the ``readings`` class attribute.
     It is supported by the ``_BACKGROUND_ID`` and ``_SAMPLE_ID`` class constants and by the ``_get_elapsed_time`` private method.
     It supports the ``process_readings`` public method.
   - **_get_net_measurements**: Processes net measurements from background and sample data and returns them as a DataFrame.
     This method calculates net measurements by subtracting background data from sample data.
     It gathers the information from the ``background`` and ``sample`` class attributes.
     It supports the ``process_readings`` public method.

3. **Summary methods**:

   - **__str__**: Returns a detailed summary of the measurements.
     This method is used to generate a string representation of the class's state.
     It gathers the information from the configuration and measurement class attributes.
     It is supported by the ``_get_readings_summary`` private method.
     It supports the ``summarize_readings`` public method.
   - **_get_readings_summary**: Generates a summary of the readings and returns it as a DataFrame.
     This method compiles key statistics and information from the parsed data.
     It gathers the information from the ``readings`` class attribute.
     It supports the ``__str__`` dunder method and the ``_get_readings_statistics`` private method.
   - **_get_readings_statistics**: Calculates statistics from the readings summary and returns them as a dictionary.
     This method provides detailed metrics for analysis.
     It is supported by the ``_get_readings_summary`` private method.
     It supports the ``parse_readings`` public method.

Helper functions
----------------

Helper functions are designed to perform specific tasks that support the main operations of the ``Hidex300`` class.
They are not part of the ``Hidex300`` class, but they are included in the ``hidex300`` module.
They handle tasks such as file retrieval, time calculations, and data plotting.
These functions are essential for the smooth operation of the class but are not intended to be directly interacted with by the end user.

Helper functions in the ``Hidex300`` class can be categorized into four main types:

1. **Utility functions**:

   - **_get_csv_files**: Retrieves a list of CSV files from a specified folder.
     This function helps in locating and listing all relevant CSV files that need to be processed.
     It supports the ``_parse_readings`` private method.
   - **_get_elapsed_time**: Calculates the elapsed time from the minimum 'End time' in a DataFrame and converts it to the specified time unit.
     This function helps in getting the measurements in terms of the elapsed time between consecutive measurements.
     It supports the ``_get_background_sample`` private method.

2. **Plotting functions**:

   - **_plot_background_sample_measurements**: Plots various quantities for background or sample measurements from the given DataFrame.
     This function generates multiple subplots to visualize different aspects of the measurements, such as
     count rate, dead time, real time, live time, counts, and counts uncertainty.
     It supports the ``_plot_background_sample_measurements`` private method.
   - **_plot_net_measurements**: Plots various quantities for net measurements from the given DataFrame.
     This function generates multiple subplots to visualize different aspects of the net measurements, such as
     count rate, counts and counts uncertainty.
     It supports the ``_plot_net_measurements`` private method.
