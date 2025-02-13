Getting started
===============

Let's say that you made a set of measurements of the radionuclide Lu-177 starting on November 2023 using a Hidex 300 SL automatic liquid scintillator counter.
The set of measurements consists on four cicles of measurements, each one with 2 repetitions.
Each repetition consists on measuring the background and the sample of Lu-177 consecutively in periods of 100 seconds.

For each cicle of measurements, the Hidex 300 SL automatic liquid scintillator counter provides a CSV file with the readings.
Here you can see an example of this CSV file.
Note that it is not a complete file, it is just a part of it extracted for illustration purposes.
See more details about these CSV file in the Topic guide.

.. code-block::

    Lu-177 HS3 301123_ciclo1
    Start Time 8:40:58
    - ROI1 Free Channel Limits 1 - 1023, Type Beta
    Counting type: Low
    Sample start
    Samp.;1
    Repe.;1
    Vial;1
    WName;A01
    CPM;83.970
    DPM;126
    TDCR;0.664
    Chemi;0.380
    Counts;140
    DTime;1.000
    Time;100
    EndTime;30/11/2023 08:44:20
    QPE;786.730
    QPI;350.220
    LumiCPS;276
    Temp;24.10
    Column 17;0
    Column 18;0
    Column 19;0
    Column 20;0
    Spectrum:;Alpha;Beta;Alpha Triple;Beta Triple
    1;0;0;0;0
    2;0;0;0;0
    (...)
    1023;0;0;0;0
    1024;0;0;0;0
    Alpha:
    0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0
    0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0
    (...)
    0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0
    0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0

.. note::

    Download the examples of Hidex 300 SL CSV file for this tutorial from
    `here <https://github.com/lmri-met/metpyrad/tree/main/dev/hidex300/test_case/input_files>`_

These measurements may be time consuming, and a lot of CSV files may be generated as a result.
These CSV files may be very long, with the information about the readings scattered across multiple lines.
So, to process all the CSV files provided by de Hidex 300 SL automatic liquid scintillator counter, the first thing you need to do is
to read these files and extract the information you need from them.
Let's see how you can do this using the ``Hidex300`` class.

.. note::

    This tutorial assumes that you have Python and MetPyRad library installed.
    If not, please check the installation tutorial.

    MetPyRad uses the pandas DataFrames to store the measurements.
    You should be familiar with pandas library to take advantage of this.
    If you are not familiar with pandas, check its
    `beginners tutorial <https://pandas.pydata.org/docs/user_guide/10min.html>`_.

Initialize the processor
------------------------

In order to process all the CSV files provided by de Hidex 300 SL automatic liquid scintillator counter,
the first thing you need to do initialize the Hidex TCDR processor.

In a Python shell, import ``Hidex300`` class from ``metpyrad``:

.. code-block:: python

    >>> from metpyrad import Hidex300

Then, initialize the ``processor`` by creating an instance of the ``Hidex300`` class.
Call the ``Hidex300`` class and providing the radionuclide name and the year and month of the measurements:

.. code-block:: python

    >>> processor = Hidex300(radionuclide='Lu-177', year=2023, month=11)

Verify that the processor has been initialized with the specified radionuclide, year, and month:

.. code-block:: python

    >>> print(processor)
    Measurements of Lu-177 on November 2023

Parse the readings
------------------

After initializing the processor, the next thing you need to do is reading CSV files provided by the Hidex 300 SL automatic liquid scintillator counter.
Let's say that you have the four CSV files in a folder called ``input_files``:

.. code-block:: console

    measurements/
        input_files/
            Lu-177_2023_11_30.csv
            Lu-177_2023_12_06.csv
            Lu-177_2023_12_12.csv
            Lu-177_2023_12_22.csv

Define the path to the folder that contains the input files:

.. code-block:: python

    >>> folder_path = 'input_files'

In these file there is a lot of information about the measurements, but you may not be interested in all of it.
You may be interested in just a few quantities for some calculation you need to do later.
To read the CSV files provided by the Hidex 300 SL automatic liquid scintillator counter and extract some quantities of interest,
use the ``processor.parse_readings()`` method:

.. code-block:: python

    >>> processor.parse_readings(folder_path)
    Found 2 CSV files in folder input_files

.. note::

    When calling the ``processor.parse_readings()`` method, Python looks for the ``input_files`` folder file in the current working directory.
    If Python cannot locate the folder, you will get an error.

    To avoid this error, import the ``os`` module, get your current working directory with the ``os.getcwd()`` method,
    and change the current working directory to the parent folder of the ``input_files`` folder with the ``os.chdir()`` method.

    If your ``input_files`` folder is inside the folder ``/home/my_user/measurements``:

    .. code-block:: python

        >>> import os
        >>> os.getcwd()
        '/home/my_user'
        >>> os.chdir('measurements')
        >>> os.getcwd()
        '/home/my_user/measurements'

Inspect the parsed readings
---------------------------

After parsing the readings from the Hidex 300 SL automatic liquid scintillator counter CSV files,
inspect the parsed readings to understand its structure and contents.
The ``processor`` store the parsed readings as a table using a pandas DataFrame,
so first you need to import pandas:

.. code-block:: python

    >>> import pandas as pd

In order to show all the columns of the DataFrame, use the ``pd.set_option()`` method:

.. code-block:: python

    >>> pd.set_option('display.max_columns', None)

Access the parsed readings by calling the ``processor.readings`` attribute:

.. code-block:: python

    >>> processor.readings
       Cycle  Sample  Repetitions  Count rate (cpm)  Counts (reading)  Dead time Real time (s)            End time
    0      1       1            1             83.97               140      1.000           100 2023-11-30 08:44:20
    1      1       2            1         252623.23            374237      1.125           100 2023-11-30 08:47:44
    2      1       1            2             87.57               146      1.000           100 2023-11-30 08:51:04
    3      1       2            2         251953.09            373593      1.124           100 2023-11-30 08:54:28
    4      2       1            1             97.77               163      1.000           100 2023-12-01 12:46:16
    5      2       2            1         223744.10            335987      1.110           100 2023-12-01 12:49:40
    6      2       1            2             85.17               142      1.000           100 2023-12-01 12:53:00
    7      2       2            2         223689.40            335843      1.110           100 2023-12-01 12:56:24

This table compiles, for each cycle and repetition, the measurements provided by the Hidex 300 SL automatic liquid scintillator counter of
count rate, counts, real time, dead time and end time, both for the radionuclide sample and the background.
See more details about these quantities in the Topics guide.

Print a summary of the readings
-------------------------------

After parsing and inspecting the readings, you can print a summary of the readings:

.. code-block:: python

    >>> print(processor)
    Measurements of Lu-177 on November 2023
    Summary
    Number of cycles: 4
    Repetitions per cycle: 2
    Time per repetition: 100 s
    Total number of measurements: 8
    Total measurement time: 800 s
    Cycles summary
       Cycle  Repetitions  Real time (s)                Date
    0      1            2            100 2023-11-30 08:44:20
    1      2            2            100 2023-12-06 10:23:19
    2      3            2            100 2023-12-12 08:41:22
    3      4            2            100 2023-12-22 08:47:48

This summary provides a detailed information about the readings,
including information for the hole set of readings as well as for each cycle in the set.
See more details about these quantities in the Topics guide.
