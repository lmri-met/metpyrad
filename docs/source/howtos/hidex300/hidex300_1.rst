How to process the Readings of the Hidex 300 SL counter
=======================================================

This guide will walk you through the steps to process the readings of the Hidex 300 SL counter using the `Hidex300` class.
You will learn how to parse measurement data from CSV files, process different types of measurements, and generate a summary of the readings.

Prerequisites
-------------

- Python installed on your system.
- Required libraries: `pandas`, `matplotlib`.
- CSV files containing the measurement data.

How to parse the readings
-------------------------

The `parse_readings` method is used to parse measurement data from CSV files in a specified folder. This method reads the CSV files, extracts relevant data, and stores it in a DataFrame.

**Example:**

.. code-block:: python

    from hidex300 import Hidex300

    # Initialize the Hidex300 instance
    processor = Hidex300(radionuclide='Lu-177', year=2023, month=11)

    # Parse readings from the specified folder
    processor.parse_readings(folder_path='/path/to/input/files/folder')

    # Check the parsed readings
    print(processor.readings)

How to process different types of measurements
-------------------------------------------------

The `process_readings` method processes different types of measurements (background, sample, net) based on the specified `kind` parameter. This method calculates various statistics and stores the processed data in corresponding attributes.

**Example:**

.. code-block:: python

    # Process background measurements
    processor.process_readings(kind='background')

    # Process sample measurements
    processor.process_readings(kind='sample')

    # Process net measurements
    processor.process_readings(kind='net')

    # Process all types of measurements
    processor.process_readings(kind='all')

How to summarize the readings
-----------------------------

The `summarize_readings` method generates and prints a summary of the readings. You can also save the summary to a text file by setting the `save` parameter to `True`.

**Example:**

.. code-block:: python

    # Print the summary of the readings
    processor.summarize_readings()

    # Save the summary to a text file
    processor.summarize_readings(save=True, folder_path='/path/to/output/folder')
