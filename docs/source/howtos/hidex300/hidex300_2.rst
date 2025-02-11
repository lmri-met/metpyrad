Visualizing and Exporting the Measurements
==========================================

This guide will walk you through the steps to visualize and export the measurements of the Hidex 300 SL counter using the `Hidex300` class.
You will learn how to export measurement data to CSV files, generate plots for different types of measurements, and save these plots as PNG files.

Prerequisites
-------------

- Python installed on your system.
- Required libraries: `pandas`, `matplotlib`.
- Parsed and processed measurement data using the `Hidex300` class.

How to export measurements as CSV
---------------------------------

The `export_table` method is used to export measurement data to CSV files. You can export different types of measurements, such as readings, background, sample, net, or all measurements.

**Example:**

.. code-block:: python

    from hidex300 import Hidex300

    # Initialize the Hidex300 instance
    processor = Hidex300(radionuclide='Lu-177', year=2023, month=11)

    # Parse and process readings (assuming this step is already done)
    processor.parse_readings(folder_path='/path/to/input/files/folder')
    processor.process_readings(kind='all')

    # Export readings to a CSV file
    processor.export_table(kind='readings', folder_path='/path/to/output/folder')

    # Export background measurements to a CSV file
    processor.export_table(kind='background', folder_path='/path/to/output/folder')

    # Export sample measurements to a CSV file
    processor.export_table(kind='sample', folder_path='/path/to/output/folder')

    # Export net measurements to a CSV file
    processor.export_table(kind='net', folder_path='/path/to/output/folder')

    # Export all measurements to a CSV file
    processor.export_table(kind='all', folder_path='/path/to/output/folder')

How to plot measurements
------------------------

The `plot_measurements` method generates plots for different types of measurements (background, sample, or net). This method helps visualize the measurement data.

**Example:**

.. code-block:: python

    # Plot background measurements
    processor.plot_measurements(kind='background')

    # Plot sample measurements
    processor.plot_measurements(kind='sample')

    # Plot net measurements
    processor.plot_measurements(kind='net')

How to export plots
-------------------

The `export_plot` method saves the generated plots as PNG files. You can export plots for background, sample, or net measurements.

**Example:**

.. code-block:: python

    # Export background measurements plot to a PNG file
    processor.export_plot(kind='background', folder_path='/path/to/output/folder')

    # Export sample measurements plot to a PNG file
    processor.export_plot(kind='sample', folder_path='/path/to/output/folder')

    # Export net measurements plot to a PNG file
    processor.export_plot(kind='net', folder_path='/path/to/output/folder')
