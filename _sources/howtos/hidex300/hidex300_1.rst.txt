How to process Hidex 300 SL readings
====================================

This guide will walk you through the steps to process the readings of the Hidex 300 SL counter using the `Hidex300` class.
You will learn how to parse measurement data from CSV files, process different types of measurements, and generate a summary of the readings.

Prerequisites:

- Python installed on your system.
- Required libraries: ``metpyrad``
- CSV files containing the measurement data.

How to parse the readings
-------------------------

To parse the measurement readings from the CSV files provided by the Hidex 300 SL counter, you need to:

- Import the ``Hidex300`` class from ``metpyrad``.
- Initialize an instance of ``Hidex300``.
- Call the ``Hidex300.parse_readings`` method providing the folder containing the CSV files.

Then, you can access the parsed readings calling the ``Hidex300.readings`` attribute.

.. code-block:: python

    >>> from metpyrad import Hidex300
    >>> processor = Hidex300(radionuclide='Lu-177', year=2023, month=11)
    >>> processor.parse_readings(folder_path='/path/to/input/files/folder')
    >>> print(processor.readings)

The returned DataFrame will look like:

.. code-block:: console

       Cycle  Sample  Repetitions  Count rate (cpm)  Counts (reading)  Dead time Real time (s)            End time
    0      1       1            1             83.97               140      1.000           100 2023-11-30 08:44:20
    1      1       2            1         252623.23            374237      1.125           100 2023-11-30 08:47:44
    2      1       1            2             87.57               146      1.000           100 2023-11-30 08:51:04
    3      1       2            2         251953.09            373593      1.124           100 2023-11-30 08:54:28
    4      2       1            1             97.77               163      1.000           100 2023-12-01 12:46:16
    5      2       2            1         223744.10            335987      1.110           100 2023-12-01 12:49:40
    6      2       1            2             85.17               142      1.000           100 2023-12-01 12:53:00
    7      2       2            2         223689.40            335843      1.110           100 2023-12-01 12:56:24


How to process different types of measurements
----------------------------------------------

Parse the measurement readings from the CSV files:

.. code-block:: python

    >>> from metpyrad import Hidex300
    >>> processor = Hidex300(radionuclide='Lu-177', year=2023, month=11)
    >>> processor.parse_readings(folder_path='/path/to/input/files/folder')

To process different types of measurements from the parsed readings, call the ``Hidex300.process_readings`` method,
setting the ``kind`` parameter to the type of measurements to process.

Then, you can access the processed measurements calling the corresponding ``Hidex300`` attribute.

Process the background measurements:

.. code-block:: python

    >>> processor.process_readings(kind='background')
    >>> print(processor.background)

The returned DataFrame will look like:

.. code-block:: console

       Cycle  Sample  Repetition  Count rate (cpm)  Counts (reading)  Dead time Real time (s)            End time  Live time (s)     Elapsed time Elapsed time (s)      Counts  Counts uncertainty  Counts uncertainty (%)
    0      1       1           1             83.97               140        1.0           100 2023-11-30 08:44:20          100.0  0 days 00:00:00              0.0  139.950000           11.830046                8.453052
    1      1       1           2             87.57               146        1.0           100 2023-11-30 08:51:04          100.0  0 days 00:06:44            404.0  145.950000           12.080977                8.277476
    2      2       1           1             92.36               154        1.0           100 2023-12-06 10:23:19          100.0  6 days 01:38:59         524339.0  153.933333           12.406987                8.059974
    3      2       1           2             87.56               146        1.0           100 2023-12-06 10:30:03          100.0  6 days 01:45:43         524743.0  145.933333           12.080287                8.277949
    4      3       1           1             82.16               137        1.0           100 2023-12-12 08:41:22          100.0 11 days 23:57:02        1036622.0  136.933333           11.701852                8.545656
    5      3       1           2             82.77               138        1.0           100 2023-12-12 08:48:04          100.0 12 days 00:03:44        1037024.0  137.950000           11.745212                8.514108
    6      4       1           1             98.36               164        1.0           100 2023-12-22 08:47:48          100.0 22 days 00:03:28        1901008.0  163.933333           12.803645                7.810276
    7      4       1           2             76.17               127        1.0           100 2023-12-22 08:54:28          100.0 22 days 00:10:08        1901408.0  126.950000           11.267209                8.875312

Process the sample measurements:

.. code-block:: python

    >>> processor.process_readings(kind='sample')
    >>> print(processor.sample)

The returned DataFrame will look like:

.. code-block:: console

       Cycle  Sample  Repetition  Count rate (cpm)  Counts (reading)  Dead time Real time (s)            End time  Live time (s)     Elapsed time Elapsed time (s)         Counts  Counts uncertainty  Counts uncertainty (%)
    0      1       2           1         252623.23            374237      1.125           100 2023-11-30 08:47:44      88.888889  0 days 00:00:00              0.0  374256.637037          611.765181                0.163461
    1      1       2           2         251953.09            373593      1.124           100 2023-11-30 08:54:28      88.967972  0 days 00:06:44            404.0  373595.922301          611.224936                0.163606
    2      2       2           1         134111.43            209724      1.066           100 2023-12-06 10:26:44      93.808630  6 days 01:39:00         524340.0  209680.159475          457.908462                0.218384
    3      2       2           2         134390.68            210125      1.066           100 2023-12-06 10:33:27      93.808630  6 days 01:45:43         524743.0  210116.760475          458.384948                0.218157
    4      3       2           1          72225.71            116255      1.035           100 2023-12-12 08:44:45      96.618357 11 days 23:57:01        1036621.0  116305.491143          341.035909                0.293224
    5      3       2           2          72340.56            116440      1.035           100 2023-12-12 08:51:27      96.618357 12 days 00:03:43        1037023.0  116490.434783          341.306951                0.292991
    6      4       2           1          25236.95             41565      1.012           100 2023-12-22 08:51:10      98.814229 22 days 00:03:26        1901006.0   41562.829381          203.869638                0.490510
    7      4       2           2          25656.06             42239      1.012           100 2023-12-22 08:57:50      98.814229 22 days 00:10:06        1901406.0   42253.063241          205.555499                0.486487

Process the net measurements:

.. code-block:: python

    >>> processor.process_readings(kind='net')
    >>> print(processor.net)

The returned DataFrame will look like:

.. code-block:: console

       Cycle  Repetition     Elapsed time  Elapsed time (s)  Count rate (cpm)        Counts  Counts uncertainty  Counts uncertainty (%)
    0      1           1  0 days 00:00:00               0.0         252539.26 374116.687037          611.879553                0.163553
    1      1           2  0 days 00:06:44             404.0         251865.52 373449.972301          611.344316                0.163702
    2      2           1  6 days 01:39:00          524340.0         134019.07 209526.226141          458.076514                0.218625
    3      2           2  6 days 01:45:43          524743.0         134303.12 209970.827142          458.544102                0.218385
    4      3           1 11 days 23:57:01         1036621.0          72143.55 116168.557810          341.236611                0.293743
    5      3           2 12 days 00:03:43         1037023.0          72257.79 116352.484783          341.508982                0.293512
    6      4           1 22 days 00:03:26         1901006.0          25138.59  41398.896047          204.271297                0.493422
    7      4           2 22 days 00:10:06         1901406.0          25579.89  42126.113241          205.864065                0.488685

Process all types of measurements:

.. code-block:: python

    >>> processor.process_readings(kind='all')
    >>> print(processor.background)
    >>> print(processor.sample)
    >>> print(processor.net)

Note that to process the background or sample measurements, the readings must be parsed first.
Similarly, to process the net measurements, the background and sample measurements must be processed first.

How to summarize the readings
-----------------------------

Parse the measurement readings from the CSV files:

.. code-block:: python

    >>> from metpyrad import Hidex300
    >>> processor = Hidex300(radionuclide='Lu-177', year=2023, month=11)
    >>> processor.parse_readings(folder_path='/path/to/input/files/folder')

To print a summary of the parsed readings, call the ``Hidex300.summarize_readings`` method.

.. code-block:: python

    >>> processor.summarize_readings()
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

To save a summary of the parsed readings to a text file, call the ``Hidex300.summarize_readings`` method,
set the parameter ``save=True`` and provide the ``folder_path`` to save the file to.

.. code-block:: python

    >>>> processor.summarize_readings(save=True, folder_path='/path/to/output/folder')

The file is saved as ``summary.txt``.