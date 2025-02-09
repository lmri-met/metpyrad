Processing the readings
=======================

In the previous section, you parsed the readings of your measurements of Lu-177 from the Hidex 300 SL automatic liquid scintillator counter CSV files.
You extracted, for each cycle and repetition, the measurements provided by the Hidex 300 SL automatic liquid scintillator counter of
count rate, counts, real time, dead time and end time, both for the radionuclide sample and the background.

But you may need some extra information about the background and sample measurements.
Also, you may need the net measurements derived from the sample and background measurements.
Let's see how you can do this using the ``Hidex300`` class.

Process background measurements
-------------------------------

Take the ``processor`` from the previous section.
Let's get some other quantities of interest from the background readings.
Process the background measurements using the ``processor.process_readings()`` method and
specifying the type of measurement you want to process:

.. code-block:: python

    processor.process_readings(kind='background')

Then inspect the processed background readings to understand its structure and contents.
The ``processor`` store the background measurements as a table using a pandas DataFrame.
Access the background measurements by calling the ``processor.background`` attribute:

.. code-block:: python

    >>> print(processor.background)

This table compiles all the quantities of interest for the background measurements for each cycle and repetition.
In addition to the quantities parsed directly from the Hidex 300 SL automatic liquid scintillator counter CSV files
(count rate, counts, real time, dead time and end time), it compiles the live time, elpased time, and counts value and uncertainty.
See more details about these quantities in the Topic guide.

.. warning::
    Update dataframe
    Add link to the Topic guide section.

.. note::

    To process the background, sample or net measurements using the ``processor.process_readings()`` method,
    you need to parse the readings first using the ``processor.parse_readings()`` method.
    Otherwise, you will get an error.

Process sample measurements
---------------------------

Next, you can process the radionuclide sample measurements in the same way you just did for the background measurements.
Just use the ``processor.process_readings()`` method specifying the type ``sample`` instead of ``background``:

.. code-block:: python

    >>> processor.process_readings(kind='sample')

Then inspect the processed sample readings by calling the ``processor.sample`` attribute:

.. code-block:: python

    >>> print(processor.sample)

.. warning::
    Update dataframe

Process net measurements
------------------------

When measuring the activity of a radionuclide,
you are often interested in the net measurements derived from the sample and background measurements,
rather than in the sample measurement itself.
You can process the radionuclide net measurements in the same way you just did for the background and sample measurements.
Just use the ``processor.process_readings()`` method specifying the type of measurements ``net``:

.. code-block:: python

    >>> processor.process_readings(kind='net')

Then inspect the net measurements by calling the ``processor.net`` attribute:

.. code-block:: python

    >>> print(processor.net)

This table compiles all the quantities of interest for the net measurements for each cycle and repetition:
elapsed time, count rate, and counts value and uncertainty.
See more details about these quantities in the Topic guide.

.. warning::
    Update dataframe
    Add link to the Topic guide section.
