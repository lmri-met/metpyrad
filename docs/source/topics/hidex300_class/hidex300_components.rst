Hidex300 class key components
=============================

The ``Hidex300`` class is composed of several types of components, each serving a specific purpose in the overall functionality of the class.
These components include attributes, public methods, and private methods. Here's a general description of each type and how they are used:

Attributes
----------

Attributes in the ``Hidex300`` class are used to store information about the measurements and their processing state.
They include details such as the radionuclide being measured, the year and month of the measurements, and DataFrames that hold the parsed and processed data.
These attributes provide a way to maintain the state of the class and make the data accessible for various operations.

Attributes in the ``Hidex300`` class can be categorized into three main types:

1. **Configuration attributes**:

   - **radionuclide**: Stores the name of the radionuclide being measured. This attribute is essential for identifying the specific radionuclide data being processed.
   - **year**: Stores the year of the measurements. This helps in organizing and filtering the data based on the year.
   - **month**: Stores the month of the measurements. Similar to the year, this attribute aids in organizing and filtering the data based on the month.

2. **Data storage attributes**:

   - **readings**: A DataFrame that holds the parsed readings from the CSV files. This attribute is the primary storage for raw measurement data.
   - **background**: A DataFrame that contains the processed background measurements. This attribute stores data specific to background radiation measurements.
   - **sample**: A DataFrame that contains the processed sample measurements. This attribute stores data specific to sample measurements.
   - **net**: A DataFrame that contains the processed net measurements. This attribute stores data that represents the net measurements after background subtraction.

3. **Measurement attributes**:

   - **cycles**: Stores the number of cycles in the measurements. This attribute is used to keep track of the measurement cycles.
   - **cycle_repetitions**: Stores the number of repetitions per cycle. This attribute helps in understanding the repetition structure of the measurements.
   - **repetition_time**: Stores the time per repetition in seconds. This attribute is crucial for time-based calculations and analysis.
   - **total_measurements**: Stores the total number of measurements. This attribute provides a count of all measurements taken.
   - **measurement_time**: Stores the total measurement time in seconds. This attribute is used to calculate the overall duration of the measurements.

Public methods
--------------

Public methods are designed to interact with the user and provide the primary interface for using the class.
These methods include functionalities for initializing the class, parsing readings from CSV files, processing different types of measurements, summarizing the data, and exporting results.
Public methods are the main tools that users will call to perform tasks and obtain results from the class.

Public methods in the ``Hidex300`` class can be categorized into four main types:

1. **Initialization methods**:

   - **__init__**: Initializes the class with the specified radionuclide, year, and month. This method sets up the initial configuration of the class.

2. **Data processing methods**:

   - **parse_readings**: Parses readings from CSV files in a specified folder. This method reads and organizes raw data into the ``readings`` attribute.
   - **process_readings**: Processes specified types of measurements (background, sample, net, or all). This method generates processed data and stores it in the respective attributes.

3. **Summary methods**:

   - **summarize_readings**: Summarizes the readings and optionally saves the summary to a text file. This method provides an overview of the processed data.
   - **__str__**: Returns a detailed summary of the measurements. This method is used to generate a string representation of the class's state.

4. **Plotting methods**:

   - **plot_measurements**: Plots the specified type of measurements (background, sample, or net). This method generates visual representations of the data for analysis.

5. **Export methods**:

   - **export_table**: Exports specified types of measurements to CSV files. This method allows users to save the processed data in a structured format.
   - **export_plot**: Exports specified types of measurement plots to PNG files. This method provides visual representations of the data.

6. **Comprehensive analysis method**:

   - **analyze_readings**: Combines parsing, processing, summarizing, and exporting into a single workflow for comprehensive analysis. This method streamlines the entire data processing workflow.

Private Methods
---------------

Private methods provide internal functionalities that support the operations of the public methods.
They handle specific tasks such as parsing the raw data, calculating statistics, generating summaries, and plotting measurements.
These methods are not intended to be called directly by the user but are essential for the internal workings of the class.
They help to modularize the code and keep the public methods clean and focused on user interactions.

Private methods in the ``Hidex300`` class can be categorized into four main types:

1. **Data parsing methods**:

   - **_parse_readings**: Parses readings from CSV files and returns a DataFrame. This method handles the detailed logic of reading and organizing raw data.

2. **Data processing methods**:

   - **_get_background_sample**: Processes background or sample measurements and returns them as a DataFrame. This method handles the specific processing logic for background and sample data.
   - **_get_net_measurements**: Processes net measurements from background and sample data and returns them as a DataFrame. This method calculates net measurements by subtracting background data from sample data.

3. **Summary methods**:

   - **_get_readings_summary**: Generates a summary of the readings and returns it as a DataFrame. This method compiles key statistics and information from the parsed data.
   - **_get_readings_statistics**: Calculates statistics from the readings summary and returns them as a dictionary. This method provides detailed metrics for analysis.

4. **Plotting methods**:

   - **_plot_background_sample_measurements**: Plots various quantities for background or sample measurements from the given DataFrame. This method generates visual representations of background and sample data.
   - **_plot_net_measurements**: Plots various quantities for net measurements from the given DataFrame. This method focuses on visualizing net measurement data.

Helper functions
----------------

Helper functions are designed to perform specific tasks that support the main operations of the ``Hidex300`` class.
They are not part of the ``Hidex300`` class, but they are included in the ``hidex300.py``.
They handle tasks such as file retrieval, time calculations, and data plotting.
These functions are essential for the smooth operation of the class but are not intended to be directly interacted with by the end user.

Helper functions in the ``Hidex300`` class can be categorized into four main types:

1. **Utility functions**:

   - **_get_csv_files**: Retrieves a list of CSV files from a specified folder. This function helps in locating and listing all relevant CSV files that need to be processed.
   - **_get_elapsed_time**: Calculates the elapsed time from the minimum 'End time' in a DataFrame and converts it to the specified time unit. This function is crucial for time-based calculations and ensuring consistency in time measurements.

2. **Plotting functions**:

   - **_plot_background_sample_measurements**: Plots various quantities for background or sample measurements from the given DataFrame. This function generates multiple subplots to visualize different aspects of the measurements, such as count rate, dead time, real time, live time, counts, and counts uncertainty.
   - **_plot_net_measurements**: Plots various quantities for net measurements from the given DataFrame. This function focuses on visualizing net counts and counts uncertainty, providing a clear view of the net measurement data.
