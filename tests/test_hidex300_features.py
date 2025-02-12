import os

import pandas as pd
import pytest

from metpyrad.hidex300 import Hidex300


class TestHidex300Analyze:

    @pytest.fixture(autouse=True)
    def setup(self, tmpdir):
        # Create an instance of Hidex300
        self.processor = Hidex300('Lu-177', 2023, 11)
        self.output_dir = tmpdir.mkdir("output")

    def test_analyze_readings_save(self):
        self.processor.analyze_readings(input_folder='./data/hidex300', time_unit='s', save=True,
                                        output_folder=self.output_dir)
        # Check if the output files were created
        assert os.path.exists(os.path.join(self.output_dir, 'Lu-177_2023_11', 'readings.csv'))
        assert os.path.exists(os.path.join(self.output_dir, 'Lu-177_2023_11', 'background.csv'))
        assert os.path.exists(os.path.join(self.output_dir, 'Lu-177_2023_11', 'sample.csv'))
        assert os.path.exists(os.path.join(self.output_dir, 'Lu-177_2023_11', 'net.csv'))
        assert os.path.exists(os.path.join(self.output_dir, 'Lu-177_2023_11', 'all.csv'))
        assert os.path.exists(os.path.join(self.output_dir, 'Lu-177_2023_11', 'summary.txt'))
        assert os.path.exists(os.path.join(self.output_dir, 'Lu-177_2023_11', 'background.png'))
        assert os.path.exists(os.path.join(self.output_dir, 'Lu-177_2023_11', 'sample.png'))
        assert os.path.exists(os.path.join(self.output_dir, 'Lu-177_2023_11', 'net.png'))


class TestHidex300Features:
    def test_repr(self):
        processor = Hidex300('Lu-177', 2023, 11)
        expected_repr = "DataProcessor(radionuclide=Lu-177, year=2023, month=11)"
        assert repr(processor) == expected_repr


class TestHidex300ProcessReadings:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.processor = Hidex300('Lu-177', 2023, 11)

        data = {
            'Cycle': [1, 1, 1, 1],
            'Sample': [1, 1, 2, 2],
            'Repetition': [1, 2, 1, 2],
            'Count rate (cpm)': [83.97, 87.57, 252623.23, 251953.09],
            'Counts (reading)': [140, 146, 374237, 373593],
            'Dead time': [1.0, 1.0, 1.125, 1.124],
            'Real time (s)': [100, 100, 100, 100],
            'End time': pd.to_datetime(
                ['2023-11-30 08:44:20', '2023-11-30 08:51:04', '2023-11-30 08:47:44', '2023-11-30 08:54:28'])
        }
        self.processor.readings = pd.DataFrame(data)

    def test_process_background(self):
        self.processor.process_readings(kind='background')
        assert self.processor.background is not None
        assert not self.processor.background.empty

    def test_process_sample(self):
        self.processor.process_readings(kind='sample')
        assert self.processor.sample is not None
        assert not self.processor.sample.empty

    def test_process_net(self):
        self.processor.process_readings(kind='background')
        self.processor.process_readings(kind='sample')
        self.processor.process_readings(kind='net')
        assert self.processor.net is not None
        assert not self.processor.net.empty

    def test_process_all(self):
        self.processor.process_readings(kind='all')
        assert self.processor.background is not None
        assert not self.processor.background.empty
        assert self.processor.sample is not None
        assert not self.processor.sample.empty
        assert self.processor.net is not None
        assert not self.processor.net.empty

    def test_invalid_kind(self):
        with pytest.raises(ValueError):
            self.processor.process_readings(kind='invalid')


class TestHidex300Exceptions:

    @pytest.fixture(autouse=True)
    def setup(self, tmpdir):
        # Create an instance of Hidex300
        self.processor = Hidex300('Lu-177', 2023, 11)

        # Mock readings data
        data = {
            'Cycle': [1, 1, 1, 1],
            'Sample': [1, 1, 2, 2],
            'Repetition': [1, 2, 1, 2],
            'Count rate (cpm)': [83.97, 87.57, 252623.23, 251953.09],
            'Counts (reading)': [140, 146, 374237, 373593],
            'Dead time': [1.0, 1.0, 1.125, 1.124],
            'Real time (s)': [100, 100, 100, 100],
            'End time': pd.to_datetime(
                ['2023-11-30 08:44:20', '2023-11-30 08:51:04', '2023-11-30 08:47:44', '2023-11-30 08:54:28'])
        }
        self.processor.readings = pd.DataFrame(data)
        self.folder = tmpdir.mkdir("folder")

    def test_process_readings_invalid_kind(self):
        with pytest.raises(ValueError,
                           match='Invalid measurement kind. Choose from "background", "sample", "net" or "all".'):
            self.processor.process_readings(kind='invalid')

    def test_parse_readings_inconsistent_repetitions(self):
        # Delete a row by index
        self.processor.readings.drop(index=1)
        with pytest.raises(ValueError, match='Repetitions per cycle are not consistent for all measurements.'):
            self.processor._parse_readings(self.folder)

    def test_get_readings_summary_inconsistent_real_time(self):
        # Modify readings to have inconsistent real time values
        self.processor.readings.loc[3, 'Real time (s)'] = 200
        with pytest.raises(ValueError,
                           match='Real time values are not consistent for all measurements. Check readings table.'):
            self.processor._get_readings_summary()

    def test_parse_readings_no_data(self):
        # Clear readings data
        self.processor.readings = None
        with pytest.raises(ValueError,
                           match='No readings data to compute readings summary. Please read the CSV files first.'):
            self.processor._get_readings_summary()

    def test_get_background_sample_no_data(self):
        # Clear readings data
        self.processor.readings = None
        with pytest.raises(ValueError,
                           match='No readings data to compute background measurements. Please read the CSV files first.'):
            self.processor._get_background_sample(kind='background')

    def test_get_net_measurements_no_data(self):
        # Clear background and sample data
        self.processor.background = None
        self.processor.sample = None
        with pytest.raises(ValueError,
                           match='No background and sample data to compute net measurements. Please process the readings first.'):
            self.processor._get_net_measurements()

    def test_compile_measurements_no_data(self):
        # Clear background, sample, and net data
        self.processor.background = None
        self.processor.sample = None
        self.processor.net = None
        with pytest.raises(ValueError,
                           match='No background, sample, and net data to compile measurements. Please process the readings first.'):
            self.processor._compile_measurements()

    def test_plot_measurements_invalid_kind(self):
        with pytest.raises(ValueError, match='Invalid measurement kind. Choose from "background", "sample", or "net".'):
            self.processor.plot_measurements(kind='invalid')

    def test_export_table_invalid_kind(self):
        self.processor.process_readings('all')
        with pytest.raises(ValueError, match='Invalid measurement kind. Choose from "readings", "background", "sample", "net", or "all".'):
            self.processor.export_table(kind='invalid', folder_path='None')

    def test_export_plot_invalid_kind(self):
        with pytest.raises(ValueError, match='Invalid measurement kind. Choose from "background", "sample", or "net".'):
            self.processor.export_plot(kind='invalid', folder_path='None')

    def test_invalid_time_unit(self):
        with pytest.raises(ValueError,
                           match='Invalid unit. Choose from seconds \("s"\), minutes \("min"\), hours \("h"\), days \("d"\), weeks \("wk"\), months \("mo"\), or years \("yr"\).'):
            self.processor.process_readings('sample', time_unit='invalid')
