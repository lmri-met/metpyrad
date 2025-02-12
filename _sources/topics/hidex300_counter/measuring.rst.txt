Making measurements
===================

One of the common uses of the Hidex 300 SL in radionuclide metrology
is to **measure the activity** of a radionuclide in terms of time.
This type of measure allows to see how the activity of the radionuclide decays over time.
From such a measure you can derive important quantities that characterize the radionuclide being measured,
such us the half-life (:math:`t_{1/2}`) of the radionuclide.

Measurement structure
---------------------

This measure involves making **repeated measurements** of the radionuclide in the same conditions along several days.
So this measure is really a set of measurements.
This set of measurements consists on a number of **cycles** of measurement, each one with a number of repetitions.
Each **repetition** consists on measuring the sample of the radionuclide and background (a measurement without sample)
during a specific period of time.

.. code-block::

    Cicle 1
        Repetition 1
            Background measurement
            Sample measurement
        Repetition 2
            Background measurement
            Sample measurement
        ...
        Repetition n
            Background measurement
            Sample measurement
    Cicle 2
        Repetition 1
            Background measurement
            Sample measurement
        Repetition 2
            Background measurement
            Sample measurement
        ...
        Repetition n
            Background measurement
            Sample measurement
    ...
    Cicle n
        Repetition 1
            Background measurement
            Sample measurement
        Repetition 2
            Background measurement
            Sample measurement
        ...
        Repetition n
            Background measurement
            Sample measurement

To make such a set of measurements, you can program the Hidex 300 SL,
configuring the number of repetitions per cycle and the measurement time per repetition.
For each cicle of measurements, the Hidex 300 SL provides a **CSV file** with the results of the measurements.

Measurement example
-------------------

This type of measurement may be time consuming. For example, take the
`Lutetium-177 radionuclide <https://www.advancingnuclearmedicine.com/knowledgebase/nuclear-medicine-facts/lutetium-177>`_.
It is commonly used in targeted radionuclide therapy for treating neuroendocrine tumours and prostate cancer.
It is a medium-energy beta emitter with an energy of 0.149 MeV.
It also emits low-energy gamma rays, which are useful for imaging and dosimetry.
It has a half-life of about 6.7 days, which is long enough to allow for transportation and preparation of
pharmaceuticals, but short enough to minimize long-term radiation exposure.

A typical measurement of this radionuclide to determine its radioactive decay over time
involves measuring one or two cycles per day during a month.
Each cycle may have about 20 - 30 repetitions of background/sample measurements during 100 seconds.
So you may end up with a total of 1200 - 3600 measurements,
33 - 100 hours of measurement time
and 30 - 60 CSV output files from the Hidex 300 SL.
