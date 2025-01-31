Tutorials
=========

The HidexTDCRProcessor
----------------------

Getting started
^^^^^^^^^^^^^^^

This tutorial introduces the basics of the ``HidexTDCRProcessor`` class and guide users through the initial setup,
including installing dependencies, initializing the processor, parsing measurement data, inspecting the parsed data, and printing a summary.
This tutorial aims to help users understand how to effectively use the class for processing and summarizing measurements of radionuclides using the Hidex TDCR system.
By the end of this tutorial, users will be able to set up the processor, parse data from CSV files, inspect the parsed data, and generate a summary of the measurements,
providing a solid foundation for further analysis and usage of the class's capabilities.

Install dependencies
""""""""""""""""""""

Before using the ``HidexTDCRProcessor`` class, ensure you have the necessary dependencies installed. You can install them using `pip`:

.. code-block:: bash
    :linenos:

    pip install metpyrad

Initialize the processor
""""""""""""""""""""""""

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
""""""""""""""""""

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
"""""""""""""""""""""""""""
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
"""""""""""""""""""""""""""""""
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