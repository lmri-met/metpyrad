Exporting measurement data
================================

Up to this point, you parsed the readings of your measurements of Lu-177 from the Hidex TDCR system CSV files,
and processed them to get the background, sample and net measurements.
You have all this information organized and stored in tables, and you made some plots of the measurements.

The next thing you may want to do is exporting the tables to text file for further processing or reporting.
You may also want to export the plots to images to be used in reports or presentations.
Let's see how you can do this using the ``HidexTDCRProcessor`` class.

Save tables
-----------

Save background measurements table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a new folder to store the measurements' results.
Let's say that you create a folder called ``output_files`` inside the ``measurements`` folder where you had the ``input_files`` folder:

.. code-block:: console

    measurements/
        input_files/
            Lu-177_2023_11_30.csv
            Lu-177_2023_11_30.csv
            Lu-177_2023_11_30.csv
            Lu-177_2023_11_30.csv
        output_files/

.. warning::

   Update file names

Take the ``processor`` from the previous section.
Define the path to the folder that contains the input files:

.. code-block:: python

    >>> folder_path = 'output_files'

Let's export the background measurements to a CSV file.
To do this, use the ``processor.export_table()`` method and
specify the type of measurement you want to process and the output folder to save the file:

.. code-block:: python

    >>> processor.export_table(kind='background', folder_path=output_folder)
    Background measurements CSV saved to "output_files" folder.

Now if you navigate to the ``output_files`` folder you will find a file called ``background.csv`` containing
all the quantities of interest for the background measurements for each cycle and repetition in CSV format:

.. code-block::

    Cycle,Sample,Repetitions,Count rate (cpm),Counts (reading),Dead time,Real time (s),End time,Live time (s),Elapsed time,Elapsed time (s),Counts,Counts uncertainty,Counts uncertainty (%)
    1,1,1,83.97,140,1.0,100,2023-11-30 08:44:20,100.0,0 days 00:00:00,0.0,139.95,11.830046491878212,8.453052155682895
    1,1,2,87.57,146,1.0,100,2023-11-30 08:51:04,100.0,0 days 00:06:44,404.0,145.95,12.080976781701056,8.277476383488219
    2,1,1,97.77,163,1.0,100,2023-12-01 12:46:16,100.0,1 days 04:01:56,100916.0,162.95,12.765187033490735,7.833806096036044
    2,1,2,85.17,142,1.0,100,2023-12-01 12:53:00,100.0,1 days 04:08:40,101320.0,141.95,11.914277149705725,8.393291405217138

.. warning::
    Update dataframe
    Add link to the Topic guide section.

.. note::

    To export measurements tables using the ``processor.export_table()`` method,
    you need to parse the readings first using the ``processor.parse_readings()`` method and
    and process the readings using the ``processor.process_readings()`` method.
    Otherwise, you will get an error.

Save sample measurements table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Next, you can export the radionuclide sample measurements in the same way you just did for the background measurements.
Just use the ``processor.export_table()`` method specifying the type ``sample`` instead of ``background``:

.. code-block:: python

    >>> processor.export_table(kind='sample', folder_path=output_folder)
    Background measurements CSV saved to "output_files" folder.

Now if you navigate to the ``output_files`` folder you will find a file called ``sample.csv`` containing
all the quantities of interest for the sample measurements for each cycle and repetition in CSV format:

.. code-block::

    Cycle,Sample,Repetitions,Count rate (cpm),Counts (reading),Dead time,Real time (s),End time,Live time (s),Elapsed time,Elapsed time (s),Counts,Counts uncertainty,Counts uncertainty (%)
    1,1,1,83.97,140,1.0,100,2023-11-30 08:44:20,100.0,0 days 00:00:00,0.0,139.95,11.830046491878212,8.453052155682895
    1,1,2,87.57,146,1.0,100,2023-11-30 08:51:04,100.0,0 days 00:06:44,404.0,145.95,12.080976781701056,8.277476383488219
    2,1,1,97.77,163,1.0,100,2023-12-01 12:46:16,100.0,1 days 04:01:56,100916.0,162.95,12.765187033490735,7.833806096036044
    2,1,2,85.17,142,1.0,100,2023-12-01 12:53:00,100.0,1 days 04:08:40,101320.0,141.95,11.914277149705725,8.393291405217138

.. warning::
    Update dataframe
    Add link to the Topic guide section.

Save net measurements table
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Next, you can export the radionuclide net measurements in the same way you just did for the background and sample measurements.
Just use the ``processor.export_table()`` method specifying the type of measurements ``net``:

.. code-block:: python

    >>> processor.export_table(kind='net', folder_path=output_folder)
    Net measurements CSV saved to "output_files" folder.

Now if you navigate to the ``output_files`` folder you will find a file called ``net.csv`` containing
all the quantities of interest for the sample measurements for each cycle and repetition in CSV format:

.. code-block::

    Cycle,Sample,Repetitions,Count rate (cpm),Counts (reading),Dead time,Real time (s),End time,Live time (s),Elapsed time,Elapsed time (s),Counts,Counts uncertainty,Counts uncertainty (%)
    1,1,1,83.97,140,1.0,100,2023-11-30 08:44:20,100.0,0 days 00:00:00,0.0,139.95,11.830046491878212,8.453052155682895
    1,1,2,87.57,146,1.0,100,2023-11-30 08:51:04,100.0,0 days 00:06:44,404.0,145.95,12.080976781701056,8.277476383488219
    2,1,1,97.77,163,1.0,100,2023-12-01 12:46:16,100.0,1 days 04:01:56,100916.0,162.95,12.765187033490735,7.833806096036044
    2,1,2,85.17,142,1.0,100,2023-12-01 12:53:00,100.0,1 days 04:08:40,101320.0,141.95,11.914277149705725,8.393291405217138

.. warning::
    Update dataframe
    Add link to the Topic guide section.

Save plots
----------

Save background measurements plot
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now that you have exported the measurement tables to CSV files, let's export the measurements plots to PNG images.
To export the background measurements plot, use the ``processor.export_plot()`` method and
specify the type of measurement you want to process and the output folder to save the file:

.. code-block:: python

    >>> processor.export_plot(kind='background', folder_path=output_folder)
    Background measurements PNG saved to "output_files" folder.

Now if you navigate to the ``output_files`` folder you will find a file called ``background.png`` containing
plots of the quantities of interest for the background measurements in terms of time:

.. warning::
    Add plot.
    Add link to the Topic guide section.

Save sample measurements plot
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Next, you can export the radionuclide sample measurements plot in the same way you just did for the background measurements.
Just use the ``processor.export_plot()`` method specifying the type ``sample`` instead of ``background``:

.. code-block:: python

    >>> processor.export_plot(kind='sample', folder_path=output_folder)
    Background measurements PNG saved to "output_files" folder.

Now if you navigate to the ``output_files`` folder you will find a file called ``sample.png`` containing
plots of the quantities of interest for the sample measurements in terms of time:

.. warning::
    Add plot.
    Add link to the Topic guide section.

Save net measurements plot
^^^^^^^^^^^^^^^^^^^^^^^^^^

Next, you can export the radionuclide net measurements plot in the same way you just did for the background and sample measurements.
Just use the ``processor.export_plot()`` method specifying the type of measurements ``net``:

.. code-block:: python

    >>> processor.export_plot(kind='net', folder_path=output_folder)
    Net measurements PNG saved to "output_files" folder.

Now if you navigate to the ``output_files`` folder you will find a file called ``net.png`` containing
plots of the quantities of interest for the net measurements in terms of time:

.. warning::
    Add plot.
    Add link to the Topic guide section.
