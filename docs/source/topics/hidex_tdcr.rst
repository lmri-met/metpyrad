Hidex TDCR processor
====================

Overview of radionuclide metrology
----------------------------------

Radionuclide metrology
^^^^^^^^^^^^^^^^^^^^^^

**Radionuclide metrology** is the science of measuring radioactivity with high precision and accuracy.
Its primary goal is to ensure the reliability and consistency of radioactivity measurements across the world
and across various applications, such as healthcare, environmental monitoring, and nuclear energy production.

National Metrology Institutes (NMIs) around the world work coordinately to this goal.
Radionuclide metrology laboratories try to met this goal through:

- **Primary standardisation techniques**:
  Using methods like liquid scintillation counting and coincidence techniques,
  they realise the SI-derived unit for activity of a radionuclide, which is the becquerel (Bq),
  and provide the most accurate measurements of activity.

- **International comparisons**:
  Through key comparisons of their standards, they demonstrate international equivalence of the activity
  measurements worldwide.

- **Secondary standardisation techniques**:
  They provide the tools needed to convert a count rate in a detector into an activity measurement traceable to the
  International System of Units (SI).
  They provide certified radioactive sources for calibration, accurate half-life values, emission
  probabilities of various types of radiation (x rays, gamma rays, alpha particles, conversion electrons, Auger
  electrons), and evaluated decay schemes of the most important radionuclides.

Find more details about radionuclide metrology in this
`JRC technical report <https://publications.jrc.ec.europa.eu/repository/handle/JRC129308>`_.

Liquid scintillation counting (LSC)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Liquid scintillation counting (LSC)** is a measuring technique for the determination of low energetic β-emitters.
It is capable to detect all processes emitting light photons, both, directly and indirectly.
Therefore, it is also applicable for high energetic β-emitters, electron capture nuclides and α-emitters.

A sample for LSC consists in a liquid scintillation cocktail,
a homogeneous solution of the active material in a liquid scintillator.
The photon emissions from the activated scintillation cocktail is counted using photomultiplier tubes.
LSC measuring efficiency is very high due to the intimate contact between sample and scintillator.

In radionuclide metrology, LSC has been successfully employed for the standardization of many radionuclides for decades.
There are two methods to do this: the CIEMAT/NIST efficiency tracing and the triple-to-double coincidence ratio (TDCR).
Both methods are accepted by Section II of the Consultative Committee for Ionization Radiation (CCIR) in
Bureau International des Poids et Mesures (BIPM) for the international reference system (SIR) for pure β-emitters.

Find more details about the LSC technique in this
`academic article by R. Broda et al. <http://doi.org/10.1088/0026-1394/44/4/S06>`_
For a more user-frindly approach, check this
`Introduction to liquid scintillation <https://www.hidex.com/hidex-methods/introduction/triple-coincidence-applications>`_.

Triple-to-double coincidence ratio (TDCR)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The **triple-to-double coincidence ratio (TDCR)** method is a fundamental method in liquid scintillation counting.
It is an absolute method for the determination of the activity of β- and EC-decaying radionuclides
in liquid scintillator medium.

It is a universal method applicable for both chemical and color quenching, for aqueous and organic samples and
for different cocktails and range of isotopes.
Unlike other methods, this method does not need external or internal standard sources.

The method itself is based on a physical and statistical model of the distribution of scintillation photons and
their detection probability in a three-photomultiplier (PMT) counter.
It combines experimental data with theoretical calculations of the detector efficiency.
The knowledge of the radionuclide decay scheme data is precondition.

Find more details about the TDCR method in this
`academic article by R. Broda <https://doi.org/10.1016/S0969-8043(03)00056-3>`_.
For a more user-frindly approach, check this
`Introduction to liquid scintillation <https://www.hidex.com/hidex-methods/introduction/triple-coincidence-applications>`_.

Overview of Hidex 300 SL
------------------------

The **Hidex 300 SL** is a an automatic liquid scintillation counter
with an automatic sample changer and a triple photomultiplier tube detection assembly.
It is used to measure the activity of liquid scintillation samples.

Key features of the Hidex 300 SL:

- **Automatic sample changer**:
  Typical scintillation vials are loaded in sample racks.
  A robotic loading arm transfer the vials from the sample racks to the measurement chamber.
- **Triple-PMT detector technology**:
  It utilizes three PMTs aligned at 120° from each other with a highly reflective measurement chamber design.
  This provide optimal measurement geometry and maximises light collection.
  Its lead shield design provides good shielding, minimizes instrument weight, and reduces background effects.
- **TDCR tecnology**:
  Absolute activity counting using triple-to-double coincidence ratio (TDCR) method.
  It also supports using an external standard method.
- **Temperature stabilization**:
  It supports measurement at a controlled temperature optimal for the scintillation cocktails used.

Find more details about this instrument in the
`Hidex website <https://www.hidex.com/products/liquid-scintillation-counters/hidex-300-sl>`_.

Calculating background, sample and net quantities
-------------------------------------------------

Output files of the HidexTDCR class
--------------------------------------------
