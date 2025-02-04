Hidex TDCRP processor
=====================

This tutorial aims to help users understand how to effectively use the ``HidexTDCRProcessor`` class
for processing the measurements of radionuclides using the Hidex TDCR system.
This tutorial provides the users with a basic understanding of the ``HidexTDCRProcessor`` class,
covering the initial setup, data processing, visualization, and exporting of measurement data.

The guide is divided into three parts:

1. **Getting started**:
   Introduce the basics of the ``HidexTDCRProcessor`` class and guide users through the initial setup.
   This part helps users to set up the processor, parse data from CSV files, inspect the parsed data, and generate a summary of the measurements, providing a solid foundation for further analysis.
2. **Processing the readings data**:
   Teach users to process different types of measurements.
   This part guides users through processing background, sample and net measurements, enabling effective handling and analysis of measurement data.
3. **Visualizing and exporting measurement data**:
   Teach users to create plots for different types of measurements and to export the measurements as files or images.
   This part help users to visualize their measurements and save their data in various formats for further analysis and presentation.

Getting started
---------------

Install dependencies
^^^^^^^^^^^^^^^^^^^^

Before using the ``HidexTDCRProcessor`` class, ensure you have the necessary dependencies installed. You can install them using `pip`:

.. code-block:: bash
    :linenos:

    pip install metpyrad

Initialize the processor
^^^^^^^^^^^^^^^^^^^^^^^^

Create an instance of the ``HidexTDCRProcessor`` class by providing the radionuclide name and the year and month of the measurements:

.. code-block:: python
    :linenos:

    from metpyrad import HidexTDCRProcessor

    # Initialize the processor
    processor = HidexTDCRProcessor(radionuclide='Lu-177', year=2023, month=11)

Verify that the processor has been initialized with the specified radionuclide, year, and month:

.. code-block:: python
    :linenos:

    print(processor)

.. code-block:: text

    Measurements of Lu-177 on November 2023

Parse the readings
^^^^^^^^^^^^^^^^^^

After instantiating the ``HidexTDCRProcessor`` class, the first thing you may want to do is
parsing the readings data from the CSV files provided by the Hidex TDCR system.
If your CSV are located in the folder ``/path/to/csv/files``, you can do this using the ``parse_readings`` method:

.. code-block:: python
    :linenos:

    # Path to the folder containing the CSV files
    folder_path = '/path/to/csv/files'

    # Parse the readings
    processor.parse_readings(folder_path)

.. code-block:: text

    Found 2 CSV files in folder /path/to/csv/files

Inspect the parsed readings
^^^^^^^^^^^^^^^^^^^^^^^^^^^

After parsing the readings, inspect the DataFrame containing the parsed readings to understand its structure and contents.
In order to show all the columns of the DataFrame, use ``pd.set_option()`` the command:

.. code-block:: python
    :linenos:

    import pandas as pd
    pd.set_option('display.max_columns', None)

    # Inspect the parsed readings
    print(processor.readings)

.. code-block:: text

       Cycle  Sample  Repetitions  Count rate (cpm)  Counts (reading)  Dead time Real time (s)            End time
    0      1       1            1             83.97               140      1.000           100 2023-11-30 08:44:20
    1      1       2            1         252623.23            374237      1.125           100 2023-11-30 08:47:44
    2      1       1            2             87.57               146      1.000           100 2023-11-30 08:51:04
    3      1       2            2         251953.09            373593      1.124           100 2023-11-30 08:54:28
    4      2       1            1             97.77               163      1.000           100 2023-12-01 12:46:16
    5      2       2            1         223744.10            335987      1.110           100 2023-12-01 12:49:40
    6      2       1            2             85.17               142      1.000           100 2023-12-01 12:53:00
    7      2       2            2         223689.40            335843      1.110           100 2023-12-01 12:56:24

Print a summary of the readings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After parsing and inspecting the readings, you can print a summary of the readings:

.. code-block:: python
    :linenos:

    # Print the summary of the measurements
    print(processor)

.. code-block:: text

    Measurements of Lu-177 on November 2023
    Summary
    Number of cycles: 2
    Repetitions per cycle: 2
    Time per repetition: 100 s
    Total number of measurements: 4
    Total measurement time: 400 s
    Cycles summary
       Cycle  Repetitions  Real time (s)                Date
    0      1            2            100 2023-11-30 08:44:20
    1      2            2            100 2023-12-01 12:46:16

This summary provides a detailed information of the readings, including the number of cycles, repetitions per cycle, total measurement time, and other relevant details.

Processing the readings data
----------------------------

Process background measurements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Process the background measurements using the ``process_readings`` method:

.. code-block:: python
    :linenos:

    # Process background measurements
    processor.process_readings(kind='background')

.. code-block:: text

    Background measurements processed successfully.

This output confirms that the background measurements have been processed.

Process sample measurements
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Next, process the sample measurements:

.. code-block:: python
    :linenos:

    # Process sample measurements
    processor.process_readings(kind='sample')

.. code-block:: text

    Sample measurements processed successfully.

This output confirms that the sample measurements have been processed.

Process net measurements
^^^^^^^^^^^^^^^^^^^^^^^^

Then, process the net measurements, which are derived from the background and sample measurements:

.. code-block:: python
    :linenos:

    # Process net measurements
    processor.process_readings(kind='net')

.. code-block:: text

    Net measurements processed successfully.

This output confirms that the net measurements have been processed.

Visualizing and exporting measurement data
------------------------------------------

Plot background measurements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create and customize a plot for the background measurements:

.. code-block:: python
    :linenos:

    # Plot background measurements
    processor.plot_measurements(kind='background')

A plot window displaying various quantities for background measurements, such as count rate, dead time, real time, live time, counts, and counts uncertainty.

Plot sample measurements
^^^^^^^^^^^^^^^^^^^^^^^^

Create and customize a plot for the sample measurements:

.. code-block:: python
    :linenos:

    # Plot sample measurements
    processor.plot_measurements(kind='sample')

A plot window displaying various quantities for sample measurements, similar to the background measurements plot.

Plot net measurements
^^^^^^^^^^^^^^^^^^^^^

Create and customize a plot for the net measurements:

.. code-block:: python
    :linenos:

    # Plot net measurements
    processor.plot_measurements(kind='net')

A plot window displaying various quantities for net measurements, such as elapsed time, counts, and counts uncertainty.

Save tables
^^^^^^^^^^^

Save the measurement data as CSV files:

.. code-block:: python
    :linenos:

    # Path to the folder where the files will be saved
    output_folder = '/path/to/output/folder'

    # Save background measurements table
    processor.export_measurements_table(kind='background', folder_path=output_folder)

    # Save sample measurements table
    processor.export_measurements_table(kind='sample', folder_path=output_folder)

    # Save net measurements table
    processor.export_measurements_table(kind='net', folder_path=output_folder)

.. code-block:: text

    Background measurements CSV saved to "/path/to/output/folder" folder.
    Sample measurements CSV saved to "/path/to/output/folder" folder.
    Net measurements CSV saved to "/path/to/output/folder" folder.

This output confirms that the tables for background, sample, and net measurements have been successfully saved as CSV files in the specified folder.

Save plots
^^^^^^^^^^

Save the measurements plots as PNG images:

.. code-block:: python
    :linenos:

    # Path to the folder where the files will be saved
    output_folder = '/path/to/output/folder'

    # Save background measurements plot
    processor.export_measurements_plot(kind='background', folder_path=output_folder)

    # Save sample measurements plot
    processor.export_measurements_plot(kind='sample', folder_path=output_folder)

    # Save net measurements plot
    processor.export_measurements_plot(kind='net', folder_path=output_folder)

.. code-block:: text

    Background measurements PNG saved to "/path/to/output/folder" folder.
    Sample measurements PNG saved to "/path/to/output/folder" folder.
    Net measurements PNG saved to "/path/to/output/folder" folder.

This output confirms that the plots for background, sample, and net measurements have been successfully saved as PNG images in the specified folder.