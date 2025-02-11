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

Parsing CSV files
^^^^^^^^^^^^^^^^^

The ``parse_readings`` method calls the ``_parse_readings`` private method to handle the detailed parsing logic,
which includes reading the files, extracting relevant data, and organizing it into a structured DataFrame.

Getting CSV files
"""""""""""""""""

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

Summarizing measurements
------------------------

With the raw data of the readings parsed and the statistics of the readings generated,
the class can generate a summary of the parsed readings in a user friendly format.
This summary includes the key aspects of the measurement cycles
as well as of the complete set of measurements including all cycles.
The ``summarize_readings`` method handles this task,
providing a concise overview of the measurements structure as well as of the class's current data and processing state.

This method can show the summary directly in the console or write it to a text file.
This behaviour is determined by the parameter ``save``.

- By default, the ``save`` parameter is set to False, then the method print the summary through the console.
- However, if the ``save`` parameter is set to ``True``, it writes the summary to a text file called ``summary.txt``
  in the folder specified in the parameter ``folder_path``.

In any case, the method calls the ``__str__`` dunder method to create the summary as a string.
The summary string generated depends on the class's current data and processing state.

- If the readings of the measurements **have not been parsed** from the Hidex 300 SL CSV files
  (meaning the ``readings`` attribute is ``None``), the method compile the information of the configuration attributes
  (radionuclide, year, month) and returns them in a readable way.
- If the readings of the measurements **have been parsed** from the Hidex 300 SL CSV files
  (meaning the ``readings`` attribute is not ``None``),
  the method compile the information of the configuration attributes, the measurement attributes
  (number of cycles, repetitions per cicle, measurement time per repetition, total number of measurements and total measurement time)
  and the summary of the measurement cycles returned by the ``_get_readings_summary`` private method and returns them in a readable way.

Processing measurements
-----------------------

With the raw data of the readings parsed and the statistics of the readings generated, the class can proceeds to process the measurements.
**Processing the readings** involves computing certain quantities of interest for the characterization of the radionuclide being measured
from the quantities extracted from the CSV files provided by the Hidex 300 SL.
This involves categorizing the data into **different types**: background measurements, sample measurements, and net measurements.

The ``process_readings`` method handles this task.
It processes different types of measurements (background, sample, net, or all)
and updates the corresponding attributes with the processed data for further use.
It calls specific private methods to handle each type of measurement and raises an error if an invalid type is provided.

The **type of measurement** to proces is defined by the ``kind`` parameter.
Options are 'background', 'sample', 'net', or 'all'.
In any case, one of the quantities to calculate is the **elapsed time** between measurements of the same type.
The user can choose the unit of this quantity setting it in the ``time_unit`` parameter.
Default is 's' (seconds). Other options include 'min' (minutes), 'h' (hours), 'd' (days), 'wk' (weeks), 'mo' (months), and 'yr' (years).

To **process background measurements**, the ``kind`` must be set to ``background``
Then the method calls the ``_get_background_sample`` with the same ``kind`` and ``time_unit`` parameters.
This method returns the processed background measurements as a DataFrame,
which is stored in the ``background`` class attribute.
The processed background measurements are stored in the ``background`` class attribute.

To **process sample measurements**, the ``kind`` must be set to ``sample``
Then the method calls the ``_get_background_sample`` with the same ``kind`` and ``time_unit`` parameters.
This method returns the processed sample measurements as a DataFrame,
which is stored in the ``sample`` class attribute.

To **process net measurements**, the ``kind`` must be set to ``net``
Then the method calls the ``_get_background_sample`` with the same ``kind`` and ``time_unit`` parameters.
This method returns the processed background measurements as a DataFrame,
which is stored in the ``net`` class attribute.

If the ``kind`` parameter is set to ``all``, the method processes all types of measurements (background, sample and net) and stores in the corresponding class attributes.

Processing background/sample measurements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``_get_background_sample`` method processes either background or sample measurements from the parsed measurement readings
and returns them as a DataFrame.
It takes a parameter ``kind`` to specify whether it is processing background or sample data.
Options are ``background`` or ``sample``.
It also take a ``time_unit`` parameter to specify the unit to calculate the elapsed time between measurements.
In the class workflow, both parameters are set by the ``process_readings`` method.

The method first **check for data availability**. If ``readings`` class attribute is ``None``, it raises a ``ValueError``,
indicating that no readings data is available.

Then, the method **filters the** ``readings`` **DataFrame** based on the ``kind`` parameter
to isolate the background or sample measurements in a new Dataframe.
In order to do this, it defines a dictionary that maps the measurement types (background and sample)
to their respective identifiers (set in the ``_BACKGROUND_ID`` and ``_SAMPLE_ID`` class constants).

It then calculates the **quantities of interest** for each repetition within each cycle from those stored in the filtered Dataframe.

- It calculates the **live time** (in seconds) by dividing the real time (in seconds) by the dead time (:math:`\ge 1`)
- It calculates the **elapsed time** between measurements in ``datetime`` format and in the specified unit
  by calling the ``_get_elapsed_time`` helper function and passing the filtered DataFrame and the specified ``time_unit``.
- It calculates the **counts** by multiplying the count rate (in counts per minute) by the live time (in seconds) and dividing by 60.
- It calculates the **counts uncertainty** as the square root of the counts.
- It calculates the **counts relative uncertainty** (in %) by dividing the counts uncertainty by the counts and multiplying by 100.

These quantities are added as new columns to the filtered DataFrame, which is then returned.

Processing net measurements
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``_get_net_measurements`` method processes net measurements from the background and sample measurements
and returns them as a DataFrame.
It takes a parameter ``time_unit`` to specify the unit to calculate the elapsed time between measurements.
In the class workflow, both parameters are set by the ``process_readings`` method.

The method first **check for data availability**. If ``background`` and ``sample`` class attribute are ``None``,
it raises a ``ValueError`` indicating that the necessary data is not available.

Then, some of the quantities **quantities of interest** for each repetition within each cycle are taken directly from the ``sample`` DataFrame:
cycle, repetition, and elapsed time in ``datetime`` format and in the specified unit.
Some other **quantities of interest** for each repetition within each cycle
from those stored in the ``background`` and ``sample`` Dataframes.

- It calculates the **net count rate** (in cpm) by subtracting the background count rate from the sample count rate.
- It calculates the **net counts** by subtracting the background counts from the sample counts.
- It calculates the **net counts uncertainty** as the square root of the sum of sample and background counts.
- It calculates the **relative net counts uncertainty** (in %) calculated as the counts uncertainty divided by the net counts and multiplied by 100.

The method compiles the results in a dictionary which is finally returned as a Dataframe.

Computing elapsed time
^^^^^^^^^^^^^^^^^^^^^^

The ``_get_elapsed_time`` method calculates the elapsed between measurements in ``datetime`` format from a specified
DataFrame (set in the ``df`` parameter) and converts it to the specified time unit (set in the ``time_unit``).
In the class workflow, both parameters are set by the ``_get_background_sample`` method.

First, the method get the **initial time** of the measurement by finding the earliest measurement end time
in the ``background`` or ``sample`` DataFrame.
Then it calculates the elapsed time between measurements by subtracting the initial_time from the end time values.
This results in a pandas Series of time deltas.

Then, the method defines a **time conversion dictionary** that maps each time unit to its corresponding conversion factor from seconds.
The next conversion factors are used:

- 1 minute = 60 seconds
- 1 hour = 60 minutes
- 1 day = 24 hours
- 1 week = 7 days
- 1 month = 30.44 days
- 1 year =  365.25 days

Then, the method **validate the time unit**, checking if the provided ``time_unit`` is present in the time conversion dictionary.
Options are 's' (seconds), 'min' (minutes), 'h' (hours), 'd' (days), 'wk' (weeks), 'mo' (months), and 'yr' (years).
If it is not, it raises a ``ValueError`` exception.

Then, the method **converts the elapsed time** from ``datetime`` to seconds using the ``datetime`` builtin function ``total_seconds()``.
Then it converts the elapsed time from seconds to the specified unit by multiplying by the corresponding time conversion factor.

Finally, the method returns a tuple containing the original elapsed time (as time deltas) and
the elapsed time converted to the specified unit.

Plotting measurements
---------------------

After parsing the readings from the CSV files provided by the Hidex 300 SL and processing the different types of
measurements, the class is ready to plot relevant information of the measurements in terms of time.

The ``plot_measurements`` method handles this task.
It uses ``matplotlib`` to generate the plots.
It determines the type of measurements to plot based on the ``kind`` parameter (``background``, ``sample``, or ``net``).
It then calls the appropriate helper function for the specified measurement type
(``_plot_background_sample_measurements`` for background or sample measurements or ``_plot_net_measurements`` for net measurements)
and providing the corresponding attribute DataFrame (``background``, ``sample``, or ``net``).
It raises a ``ValueError`` if an invalid ``kind`` is provided.

Plotting background or sample measurements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``_plot_background_sample_measurements`` helper function creates a series of plots for background or sample measurements.
It determines the type of measurements to plot based on the ``kind`` parameter (``background`` or ``sample``).
It gathers the measurements data from the corresponding attribute DataFrame (``background``, ``sample``, or ``net``).
In the class workflow, both parameters are set by the ``plot_measurements`` method.

It extracts the ``End time`` column from the appropriate measurement DataFrame for the x-axis.
Then it creates a 3x2 grid of subplots to plot the next quantities in terms of the end time:
count rate, dead time, real time, live time, counts, and counts uncertainty,
extracting the corresponding column from the appropriate measurement DataFrame.
It set the x-axis labels ``End time`` and the y-axis labels to the corresponding quantity and unit.
It sets the title of the figure to ``Background  measurements`` or ``Sample  measurements``
depending on the kind of measurement to plot.

Plotting net measurements
^^^^^^^^^^^^^^^^^^^^^^^^^

The ``_plot_net_measurements`` helper function creates a series of plots for net measurements.
It gathers the measurements data from the ``net`` attribute DataFrame
In the class workflow, this parameter is set by the ``plot_measurements`` method.

It extracts the ``Elapsed time`` (with its unit) column from the attribute DataFrame for the x-axis.
Then it creates a 2x1 grid of subplots to plot the next quantities in terms of the elapsed time:
counts and counts uncertainty,
extracting the corresponding column from the attribute DataFrame.
It set the x-axis labels ``Elapsed time`` (with its unit) and the y-axis labels to the corresponding quantity and unit.
It sets the title of the figure to ``Net quantities measurements``.

Exporting measurements
----------------------

After parsing the readings from the CSV files provided by the Hidex 300 SL and processing the different types of
measurements, the class is ready to save the processed data and visualizations to CSV and PNG files for further analysis and reporting.

Exporting tables
^^^^^^^^^^^^^^^^

The ``export_table`` method saves specified types of measurements as a CSV file to the specified folder path.
It determines the type of measurements to plot based on the ``kind`` parameter
(``readings``, ``background``, ``sample``, ``net``, or ``all``).

First, the method maps the ``kind`` parameter to the corresponding DataFrame attributes (``readings``, ``background``,
``sample``, ``net``, or a the compiled DataFrame returned by the ``_compile_measurements`` method for ``all``).
Then, it validates the ``kind`` parameter by ensuring it exists in the dictionary keys.
If the ``kind`` is invalid, it raises a ``ValueError`` exception.

Then, it retrieves the corresponding DataFrame from the dictionary and
exports it to a CSV file in the specified ``folder_path`` using the ``to_csv`` method of the DataFrame.
The CSV file is named after the ``kind`` parameter.
Finally, it prints a confirmation message indicating the successful export.

Exporting plots
^^^^^^^^^^^^^^^

The ``export_plot`` method class saves the plot of a specified type of measurements as a PNG file to the specified folder path.
It determines the type of measurements to plot based on the ``kind`` parameter
(``background``, ``sample``, or ``net``).

First, the method maps the ``kind`` parameter to the corresponding DataFrame attributes (``readings``, ``background`` or ``sample``).
Then, it validates the ``kind`` parameter by ensuring it exists in the dictionary keys.
If the ``kind`` is invalid, it raises a ``ValueError`` exception.

Then, it calls the ``plot_measurements`` method to generate the plot and
exports it to a PNG file in the specified ``folder_path`` using the ``savefig`` method of ``matplotlib``.
The PNG file is named after the ``kind`` parameter.
Finally, it prints a confirmation message indicating the successful export.

Comprehensive analysis
----------------------

The ``Hidex300`` class allows to run a full comprehensive analysis of the readings,
combining all the previous steps into a single workflow, including
including parsing, processing and summarizing the readings and exporting the results to CSV and PNG files.
The ``analyze_readings`` method handles this task.

First, the method **parses the readings** of the CSV files provided by the Hidex 300 SL from the specified
``input_folder``, by calling the calling the ``parse_readings`` method.
Then, it **processes all types of measurements** (background, sample and net) by calling the ``process_readings``
method with ``kind='all'`` and the specified ``time_unit``.
Finally, it **prints a summary** of the measurements by calling the ``__str__`` method.

Optionally, the method can **save the results** (CSV files and plots) to the specified ``output_folder``
if the ``save`` parameter is ``True``.
The method checks if the ``output_folder`` exists and creates it if it doesn't.
It also creates a subfolder for the specific radionuclide, year, and month to store the results.
Then it saves the background, sample, net, and compiled measurements as CSV files to this folder
by calling the ``export_table`` method.
It also saves the summary of the readings to a text file by calling the ``summarize_readings``.
Finally, it saves plots of background, sample, and net measurements to PNG files by calling the ``export_plot`` method.
