Exporting measurement data
================================

Up to this point, you parsed the readings of your measurements of Lu-177 from the Hidex 300 SL automatic liquid scintillator counter CSV files,
and processed them to get the background, sample and net measurements.
You have all this information organized and stored in tables, and you made some plots of the measurements.

The next thing you may want to do is exporting the tables to text file for further processing or reporting.
You may also want to export the plots to images to be used in reports or presentations.
Let's see how you can do this using the ``Hidex300`` class.

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
            Lu-177_2023_12_06.csv
            Lu-177_2023_12_12.csv
            Lu-177_2023_12_22.csv
        output_files/

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

    Cycle,Sample,Repetition,Count rate (cpm),Counts (reading),Dead time,Real time (s),End time,Live time (s),Elapsed time,Elapsed time (s),Counts,Counts uncertainty,Counts uncertainty (%)
    1,1,1,83.97,140,1.0,100,2023-11-30 08:44:20,100.0,0 days 00:00:00,0.0,139.95,11.830046491878212,8.453052155682895
    1,1,2,87.57,146,1.0,100,2023-11-30 08:51:04,100.0,0 days 00:06:44,404.0,145.95,12.080976781701056,8.277476383488219
    2,1,1,92.36,154,1.0,100,2023-12-06 10:23:19,100.0,6 days 01:38:59,524339.0,153.93333333333334,12.40698727868024,8.059974412308515
    2,1,2,87.56,146,1.0,100,2023-12-06 10:30:03,100.0,6 days 01:45:43,524743.0,145.93333333333334,12.080286972308784,8.277949044524064
    3,1,1,82.16,137,1.0,100,2023-12-12 08:41:22,100.0,11 days 23:57:02,1036622.0,136.93333333333334,11.701851705321399,8.545656065229844
    3,1,2,82.77,138,1.0,100,2023-12-12 08:48:04,100.0,12 days 00:03:44,1037024.0,137.95,11.745211790342479,8.5141078581678
    4,1,1,98.36,164,1.0,100,2023-12-22 08:47:48,100.0,22 days 00:03:28,1901008.0,163.93333333333334,12.803645314258487,7.810275710202412
    4,1,2,76.17,127,1.0,100,2023-12-22 08:54:28,100.0,22 days 00:10:08,1901408.0,126.95,11.267209059922514,8.875312374889731

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

    Cycle,Sample,Repetition,Count rate (cpm),Counts (reading),Dead time,Real time (s),End time,Live time (s),Elapsed time,Elapsed time (s),Counts,Counts uncertainty,Counts uncertainty (%)
    1,2,1,252623.23,374237,1.125,100,2023-11-30 08:47:44,88.88888888888889,0 days 00:00:00,0.0,374256.63703703706,611.7651812885701,0.16346141143464313
    1,2,2,251953.09,373593,1.124,100,2023-11-30 08:54:28,88.9679715302491,0 days 00:06:44,404.0,373595.9223013048,611.2249359289139,0.1636058906006906
    2,2,1,134111.43,209724,1.066,100,2023-12-06 10:26:44,93.80863039399624,6 days 01:39:00,524340.0,209680.15947467164,457.9084618945927,0.21838425869277625
    2,2,2,134390.68,210125,1.066,100,2023-12-06 10:33:27,93.80863039399624,6 days 01:45:43,524743.0,210116.76047529702,458.38494791528336,0.2181572507011761
    3,2,1,72225.71,116255,1.035,100,2023-12-12 08:44:45,96.61835748792271,11 days 23:57:01,1036621.0,116305.49114331724,341.03590887664194,0.29322425409510633
    3,2,2,72340.56,116440,1.035,100,2023-12-12 08:51:27,96.61835748792271,12 days 00:03:43,1037023.0,116490.43478260869,341.30695097318,0.2929913959117054
    4,2,1,25236.95,41565,1.012,100,2023-12-22 08:51:10,98.81422924901186,22 days 00:03:26,1901006.0,41562.82938076417,203.86963820236736,0.4905095279599058
    4,2,2,25656.06,42239,1.012,100,2023-12-22 08:57:50,98.81422924901186,22 days 00:10:06,1901406.0,42253.06324110672,205.55549917505667,0.48648661992174325

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

    Cycle,Repetition,Elapsed time,Elapsed time (s),Count rate (cpm),Counts,Counts uncertainty,Counts uncertainty (%)
    1,1,0 days 00:00:00,0.0,252539.26,374116.68703703705,611.8795527201714,0.16355313032577887
    1,2,0 days 00:06:44,404.0,251865.52,373449.9723013048,611.3443156694146,0.16370179703110896
    2,1,6 days 01:39:00,524340.0,134019.07,209526.22614133832,458.076514141475,0.21862490561562173
    2,2,6 days 01:45:43,524743.0,134303.12,209970.8271419637,458.5441023594463,0.21838467209991003
    3,1,11 days 23:57:01,1036621.0,72143.55,116168.5578099839,341.2366106921275,0.29374265905089897
    3,2,12 days 00:03:43,1037023.0,72257.79,116352.48478260869,341.50898199404463,0.29351240983990595
    4,1,22 days 00:03:26,1901006.0,25138.59,41398.89604743083,204.27129684343197,0.4934220869305253
    4,2,22 days 00:10:06,1901406.0,25579.890000000003,42126.11324110672,205.86406495818233,0.4886851625259837

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
plots of the quantities of interest for the background measurements in terms of time.

Save sample measurements plot
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Next, you can export the radionuclide sample measurements plot in the same way you just did for the background measurements.
Just use the ``processor.export_plot()`` method specifying the type ``sample`` instead of ``background``:

.. code-block:: python

    >>> processor.export_plot(kind='sample', folder_path=output_folder)
    Background measurements PNG saved to "output_files" folder.

Now if you navigate to the ``output_files`` folder you will find a file called ``sample.png`` containing
plots of the quantities of interest for the sample measurements in terms of time.

Save net measurements plot
^^^^^^^^^^^^^^^^^^^^^^^^^^

Next, you can export the radionuclide net measurements plot in the same way you just did for the background and sample measurements.
Just use the ``processor.export_plot()`` method specifying the type of measurements ``net``:

.. code-block:: python

    >>> processor.export_plot(kind='net', folder_path=output_folder)
    Net measurements PNG saved to "output_files" folder.

Now if you navigate to the ``output_files`` folder you will find a file called ``net.png`` containing
plots of the quantities of interest for the net measurements in terms of time.
