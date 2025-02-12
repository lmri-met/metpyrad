# MetPyRad

## Tools for radionuclide metrology

> **WARNING**: This package is under development. The public API should not be considered stable.

![Static Badge](https://img.shields.io/badge/Date-Feb_25-teal)
![Static Badge](https://img.shields.io/badge/Version-0.0.1-teal)
![Static Badge](https://img.shields.io/badge/Maintenance-Active-teal)

[![Static Badge](https://img.shields.io/badge/Surce_code-GitHub-blue)](https://github.com/lmri-met/metpyrad)
[![Static Badge](https://img.shields.io/badge/Documentation-GitHub_Pages-blue)](https://lmri-met.github.io/metpyrad/)
[![Static Badge](https://img.shields.io/badge/Contribute-Issues-blue)](https://github.com/lmri-met/metpyrad/issues)
[![Static Badge](https://img.shields.io/badge/Organization-LMRI--Met-blue)](https://github.com/lmri-met/)

[![Static Badge](https://img.shields.io/badge/Distribution-PyPi-orange)](https://pypi.org/project/metpyrad/)
[![Static Badge](https://img.shields.io/badge/License-GPLv3.0-orange)](https://choosealicense.com/licenses/gpl-3.0/)
![Static Badge](https://img.shields.io/badge/Tests-Passing-green)
![Static Badge](https://img.shields.io/badge/CodeCov-99%25-green)

## Table of Contents

- [What is MetPyRad?](#what-is-metpyrad)
- [Main features of MetPyRad](#main-features)
- [How to install MetPyRad?](#installation)
- [Quick user guide](#quick-user-guide)
- [Future developments](#future-developments)
- [How to get support?](#how-to-get-support)
- [Documentation](#documentation)
- [Contributors](#contributors)
- [License](#license)
- [Contributing to MetPyRad](#contributing-to-metpyrad)

## What is MetPyRad?

**MetPyRad** is a Python package that provides a collection of tools for radionuclide metrology.
It is an open source, GPLv3-licensed library for the Python programming language.
It is compatible with Python 3.
**MetPyRad** provides tools for processing measurements for a given radionuclide using a **Hidex 300 SL** 
automatic liquid scintillation counter.
It is designed to facilitate the handling, analysis, and summarization of measurement data.

## Main features of MetPyRad

**MetPyRad** provides five main features for processing measurements for a given radionuclide using a Hidex TDCR system:

- **Data Parsing and Processing**: It includes tools to parse measurement data from CSV files,
  process different types of measurements (background, sample, net),
  and compile the results into comprehensive data structures.
- **Measurement Summarization**: It includes tools to generate detailed summaries of the measurements,
  including statistical analysis and cycle information.
- **Visualization**: It includes plotting tools to visualize various quantities of the measurements,
  such as count rates, dead times, and uncertainties, making it easier to interpret the data.
- **Exporting Results**: It includes tools to export the processed data and visualizations to CSV and PNG files,
  for further analysis or reporting.
- **Comprehensive Analysis**: It supports end-to-end analysis workflows,
  from parsing raw data to generating summaries and visualizations, and saving the results.

## How to install MetPyRad?

**MetPyRad** can be installed from the [Python Package Index (PyPI)](https://pypi.org/project/metpyrad/)
by running the following command from a terminal:

```bash
pip install metpyrad
```

## Quick user guide

Consider that we made a **measurement** of the **radionuclide** Lu-177 starting on November 2023 using a 
**Hidex 300 SL** automatic liquid scintillation counter.
The measurement consists on a series cicles of measurements, each one with a number of repetitions.
Each repetition consists on measuring the background and the sample of Lu-177 consecutively in periods of 100 seconds.
For each cicle of measurements, Hidex TDCR system provides a **CSV file** with the readings.

We want to **process the reading files** provided by the Hidex 300 SL automatic liquid scintillation counter,
and get some quantities of interest that characterizes the activity of the radionuclide in terms of time.
The tool that **MetPyRad** provides to do this is the **HidexTDCR** class.
It allows performing a comprehensive analysis of the measurements, including parsing the files, 
processing, summarizing and visualizing the measurements, and exporting the results.

Here is a code snippet to process the readings of a set in CSV files the Hidex 300 SL stored in the folder `input_file`,
exporting the different types of measurements (background, sample and net) to CSV files and 
plots of these measurements to PNG files.

```python
from metpyrad import Hidex300
processor = Hidex300(radionuclide='Lu-177', year=2023, month=11)
processor.analyze_readings(input_folder='input_files', time_unit='s', save=True, output_folder='output')
print(processor.sample)
```

Output:
```
Processing readings from input_files.
Found 2 CSV files in folder input_files
Measurements summary:
Measurements of Lu-177 on November 2023
Summary
Number of cycles: 2
Repetitions per cycle: 2
Time per repetition: 100 s
Total number of measurements: 4
Total measurement time: 400 s
Cycles summary
   Cycle  Repetitions  Real time (s)                Date
0      1            2            100 2023-11-30 08:44:20
1      2            2            100 2023-12-01 12:46:16
Saving measurement files to folder output/Lu-177_2023_11.
Saving CSV files
Readings measurements CSV saved to "output/Lu-177_2023_11" folder.
Background measurements CSV saved to "output/Lu-177_2023_11" folder.
Sample measurements CSV saved to "output/Lu-177_2023_11" folder.
Net measurements CSV saved to "output/Lu-177_2023_11" folder.
All measurements CSV saved to "output/Lu-177_2023_11" folder.
Summary saved to output/Lu-177_2023_11/summary.txt
Saving figures
Background measurements PNG saved to "output/Lu-177_2023_11" folder.
Sample measurements PNG saved to "output/Lu-177_2023_11" folder.
Net measurements PNG saved to "output/Lu-177_2023_11" folder.
```

Example of exported table for the sample measurements:
 ```
Sample measurements
 Cycle  Sample  Repetitions  Count rate (cpm)  Counts (reading)  Dead time Real time (s)            End time  Live time (s)    Elapsed time Elapsed time (s)         Counts  Counts uncertainty  Counts uncertainty (%)
     1       2            1         252623.23            374237      1.125           100 2023-11-30 08:47:44      88.888889 0 days 00:00:00              0.0  374256.637037          611.765181                0.163461
     1       2            2         251953.09            373593      1.124           100 2023-11-30 08:54:28      88.967972 0 days 00:06:44            404.0  373595.922301          611.224936                0.163606
     2       2            1         223744.10            335987      1.110           100 2023-12-01 12:49:40      90.090090 1 days 04:01:56         100916.0  335952.102102          579.613753                0.172529
     2       2            2         223689.40            335843      1.110           100 2023-12-01 12:56:24      90.090090 1 days 04:08:40         101320.0  335869.969970          579.542897                0.172550 
```

Example of exported plot for the sample measurements:

<img src="docs/source/_static/hidex300/sample.png" alt="sample measurements" width="500"/>

## Future developments

- Add support to compute the half-live of the radionuclide from time measurements of the activity.
- Add support to process output files for other measuring instruments.

## How to get support?

If you need support, please check the **MetPyRad** documentation at GitHub
([README](https://github.com/lmri-met/metpyrad/blob/main/README.md)).

If you need further support, please send an e-mail to
[Xandra Campo](mailto:xandra.campo@ciemat.es).

## Documentation

The official documentation of **MetPyRad** is hosted on [GitHub Pages](https://lmri-met.github.io/metpyrad/).

## Contributors

**MetPyRad** is developed and maintained by [Xandra Campo](https://github.com/xandratxan/),
with the support of Nuria Navarro and Virginia Peyres.
It is one of the projects of the [Ionizing Radiation Metrology Laboratory (LMRI)](https://github.com/lmri-met/),
which is the Spanish National Metrology Institute for ionizing radiation.

## License

**MetPyRad** is distributed under the [GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/) License.

## Contributing to MetPyRad

All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.
Please check the **MetPyRad** [issues page](https://github.com/lmri-met/metpyrad/issues) if you want to contribute.