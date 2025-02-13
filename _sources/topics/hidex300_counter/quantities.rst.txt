Processing the measurements
===========================

In this section we summarize the **quantities of interest** for characterizing the radioactive decay over time for a radionuclide.
It shows which of tese quantities can be found in the output CSV files provided by the Hidex 300 SL automatic scintillator counter.
It also shows how to obtain the rest of them, including uncertainty determination.

Measured quantities
-------------------

Suppose we have a set of :math:`n` measurements for the background and a set of another :math:`n` measurements for the sample.
For each measurement :math:`i` of the background and sample, the Hidex 300 SL provides the next quantities of interest
for characterizing the radioactive decay over time for a radionuclide:

**Measurement time**, :math:`t_r`:
    The total duration for which the sample is measured, expressed in seconds (`s`).
    It is the time interval during which the detector is actively counting events.
    It is labeled as ``Time`` in the Hidex 300 SL output CSV file.

**Measurement end time**, :math:`t_{end}`:
    The specific time at which the measurement is completed, expressed in `d/m/yr h:min:s`.
    It marks the end of the measurement period.
    It is labeled as ``EndTime`` in the Hidex 300 SL output CSV file.

**Dead time**, :math:`t_d`:
    The period after each detected event during which the detector is unable to record another event.
    This is due to the time required for the detector to reset and be ready for the next event.
    It is expressed as factor :math:`\ge 1`, with 1 meaning there is no dead time in the measurement.
    It is labeled as ``DTime`` in the Hidex 300 SL output CSV file.

**Count rate**, :math:`C_r`:
    The number of counts detected per unit time, expressed in counts per minute (`cpm`).
    It indicates the activity level of the sample being measured.
    It is labeled as ``CPM`` in the Hidex 300 SL output CSV file.

Derived quantities
------------------

Now, for each measurement :math:`i` of the background and sample, we can derive the next quantities of interest
from that provided by the Hidex 300 SL:

**Live time**, :math:`t_l`:
    The actual time during which the detector is capable of recording events, excluding the dead time.
    It is expressed in seconds (`s`).
    It represents the effective counting time.
    It is calculated as the ratio of the measurement time, :math:`t_r`, and the dead time, :math:`t_d`:

    .. math::

        t_l=\frac{t_r}{t_d}

**Elapsed time**, :math:`t`:
    The total time from the start to the end of the measurement, including both live time and dead time.
    It is expressed in seconds (`s`).
    It is calculated as the difference between the end time of the measurement :math:`i`, :math:`t_{{end}_i}`
    and the end time of the first measurement, :math:`t_{{end}_{i=0}}`:

    .. math::

        t_i=t_{{end}_i}-t_{{end}_{i=0}}

**Counts**, :math:`C`:
    The total number of detected events during the measurement period, expressed in `counts`.
    It is the sum of all counts recorded over the entire measurement time.
    It is calculated as the product of the count rate, :math:`C_r`, and the live time, :math:`t_l`:

    .. math::

        C=C_r\cdot t_l

**Counts uncertainty**, :math:`u(C)`:
    The statistical uncertainty associated with the number of counts recorded, expressed in `counts`.
    It reflects the variability or error in the count measurement.
    It is computed as the square root of the counts, :math:`C`:

    .. math::

        u(C)=\sqrt{C}

    .. note::

        In radioactive decay and counting processes, the number of counts follows a Poisson distribution.
        For a Poisson-distributed variable, the mean (:math:`\lambda`) and the variance (:math:`\sigma^2`) are equal.
        The standard deviation, :math:`\sigma`, is the square root of the variance.
        Therefore, for a Poisson process, the standard deviation is :math:`\sigma=\sqrt{\lambda}`.

**Counts relative uncertainty**, :math:`u_r(C)`:
    The counts uncertainty expressed as a percentage of the total counts.
    It provides a relative measure of the uncertainty in the count data.
    It is calculated as the ratio of the counts uncertainty, :math:`u(C)`, and the counts, :math:`C`:

    .. math::

        u_r(C)=\frac{u(C)}{C}\cdot 100

Net quantities
--------------

Next, we need to determine the net quantities.
These quantities are necessary to accurately determine the activity of the sample by eliminating the influence of background radiation.
Net quantities refer to the values obtained after subtracting background counts from the measured counts.

So, for each background measurement :math:`i` and its corresponding sample measurement :math:`i`,
we can derive the next net quantities of interest:

**Net counts**, :math:`C`:
    The total counts after subtracting the background counts, expressed in `counts`.
    It is calculated as the difference between the counts of the sample, :math:`C_s`, and the counts of the background, :math:`C_b`:

    .. math::

        C=C_s-C_b

**Net counts uncertainty**, :math:`u(C)`:
    The statistical uncertainty associated with the net counts, expressed in `counts`.
    It is calculated using the propagation of uncertainty formula for subtraction:

    .. math::

        u(C)=\sqrt{u^2(C_s)-u^2(C_b)}=\sqrt{(\sqrt{C_s})^2+(\sqrt{C_b})^2}=\sqrt{C_s+C_b}

**Net counts relative uncertainty**, :math:`u_r(C)`:
    The net counts uncertainty expressed as a percentage of the net counts.
    It is calculated dividing the net counts, :math:`C`, by the net counts uncertainty, :math:`u(C)`,
    and multiplying by 100 to express it as a percentage:

    .. math::

        u_r(C)=\frac{u(C)}{C}\cdot 100

Find more details about the uncertainty determination for activity measurements in this
`article by K. Kossert et al. <https://doi.org/10.1016/j.apradiso.2012.02.084>`_.
