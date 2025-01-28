from io import StringIO

import pandas as pd
import pytest

from metpyrad.hidex_tdcr import HidexTDCRProcessor


class TestHidexTDCRProcessor:
    @pytest.fixture
    def processor(self):
        processor = HidexTDCRProcessor(radionuclide='Lu-177', year=2023, month=11)
        processor.process_readings(folder_path='./data/hidex_tdcr', time_unit='s', save=False)
        return processor

    @pytest.fixture
    def expected_summary(self):
        csv_string = """Cicle,Repetitions,Real time (s),Date
        1,2,100,2023-11-30 08:44:20
        2,2,100,2023-12-01 12:46:16
        """
        df = pd.read_csv(StringIO(csv_string))
        df[df.columns[-1]] = pd.to_datetime(df[df.columns[-1]], format='%Y-%m-%d %H:%M:%S')
        return df

    @pytest.fixture
    def expected_readings(self):
        csv_string = """Cicle,Sample,Repetitions,Count rate (cpm),Counts (reading),Dead time (s),Real time (s),End time
        1,1,1,83.97,140,1.0,100,2023-11-30 08:44:20
        1,2,1,252623.23,374237,1.125,100,2023-11-30 08:47:44
        1,1,2,87.57,146,1.0,100,2023-11-30 08:51:04
        1,2,2,251953.09,373593,1.124,100,2023-11-30 08:54:28
        2,1,1,97.77,163,1.0,100,2023-12-01 12:46:16
        2,2,1,223744.1,335987,1.11,100,2023-12-01 12:49:40
        2,1,2,85.17,142,1.0,100,2023-12-01 12:53:00
        2,2,2,223689.4,335843,1.11,100,2023-12-01 12:56:24
        """
        df = pd.read_csv(StringIO(csv_string))
        df[df.columns[-1]] = pd.to_datetime(df[df.columns[-1]], format='%Y-%m-%d %H:%M:%S')
        return df

    @pytest.fixture
    def expected_background(self):
        csv_string = """Cicle,Sample,Repetitions,Count rate (cpm),Counts (reading),Dead time (s),Real time (s),End time,Live time (s),Counts,Counts uncertainty,Counts uncertainty (%)
        1,1,1,83.97,140,1.0,100,2023-11-30 08:44:20,99.0,139.95,11.830046491878212,8.453052155682895
        1,1,2,87.57,146,1.0,100,2023-11-30 08:51:04,99.0,145.95,12.080976781701056,8.277476383488219
        2,1,1,97.77,163,1.0,100,2023-12-01 12:46:16,99.0,162.95,12.765187033490735,7.833806096036044
        2,1,2,85.17,142,1.0,100,2023-12-01 12:53:00,99.0,141.95,11.914277149705725,8.393291405217138
        """
        df = pd.read_csv(StringIO(csv_string))
        df[df.columns[7]] = pd.to_datetime(df[df.columns[7]], format='%Y-%m-%d %H:%M:%S')
        return df

    @pytest.fixture
    def expected_sample(self):
        csv_string = """Cicle,Sample,Repetitions,Count rate (cpm),Counts (reading),Dead time (s),Real time (s),End time,Live time (s),Counts,Counts uncertainty,Counts uncertainty (%)
        1,2,1,252623.23,374237,1.125,100,2023-11-30 08:47:44,98.875,421038.7166666667,648.8749622744483,0.15411289665034722
        1,2,2,251953.09,373593,1.124,100,2023-11-30 08:54:28,98.876,419921.81666666665,648.0137472821597,0.15431771381303394
        2,2,1,223744.1,335987,1.11,100,2023-12-01 12:49:40,98.89,372906.8333333333,610.6609806867746,0.16375698327333088
        2,2,2,223689.4,335843,1.11,100,2023-12-01 12:56:24,98.89,372815.6666666667,610.5863302323977,0.1637770042476034
        """
        df = pd.read_csv(StringIO(csv_string))
        df[df.columns[7]] = pd.to_datetime(df[df.columns[7]], format='%Y-%m-%d %H:%M:%S')
        return df

    @pytest.fixture
    def expected_net(self):
        csv_string = """Elapsed time,Elapsed time (s),Count rate (cpm),Counts,Counts uncertainty,Counts uncertainty (%)
        0 days 00:00:00,0.0,252539.26,420898.76666666666,648.9827938140322,0.15418975896596013
        0 days 00:06:44,404.0,251865.52,419775.86666666664,648.1263508504084,0.15439819253951279
        1 days 04:01:56,100916.0,223646.33000000002,372743.8833333333,610.7943871167557,0.16386436221423956
        1 days 04:08:40,101320.0,223604.22999999998,372673.7166666667,610.7025598985701,0.16387057433535226
        """
        df = pd.read_csv(StringIO(csv_string))
        df[df.columns[0]] = pd.to_timedelta(df[df.columns[-0]])
        return df

    def test_radionuclide(self, processor):
        assert processor.radionuclide == 'Lu-177'

    def test_year(self, processor):
        assert processor.year == 2023

    def test_month(self, processor):
        assert processor.month == 11

    def test_cycles(self, processor):
        assert processor.cycles == 2

    def test_cycle_repetitions(self, processor):
        assert processor.cycle_repetitions == 2

    def test_repetition_time(self, processor):
        assert processor.repetition_time == 100

    def test_measurements(self, processor):
        assert processor.measurements == 4

    def test_measurement_time(self, processor):
        assert processor.measurement_time == 400

    def test_summary(self, processor, expected_summary):
        pd.testing.assert_frame_equal(processor.summary, expected_summary)

    def test_readings(self, processor, expected_readings):
        pd.testing.assert_frame_equal(processor.readings, expected_readings)

    def test_background(self, processor, expected_background):
        pd.testing.assert_frame_equal(processor.background, expected_background)

    def test_sample(self, processor, expected_sample):
        pd.testing.assert_frame_equal(processor.sample, expected_sample)

    def test_net(self, processor, expected_net):
        pd.testing.assert_frame_equal(processor.net, expected_net)
