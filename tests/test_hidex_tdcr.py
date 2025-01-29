from io import StringIO

import pandas as pd
import pytest

from metpyrad.hidex_tdcr import HidexTDCRProcessor

summary = """
Cycle,Repetitions,Real time (s),Date
1,2,100,2023-11-30 08:44:20
2,2,100,2023-12-01 12:46:16
"""
readings = """
Cycle,Sample,Repetitions,Count rate (cpm),Counts (reading),Dead time,Real time (s),End time
1,1,1,83.97,140,1.0,100,2023-11-30 08:44:20
1,2,1,252623.23,374237,1.125,100,2023-11-30 08:47:44
1,1,2,87.57,146,1.0,100,2023-11-30 08:51:04
1,2,2,251953.09,373593,1.124,100,2023-11-30 08:54:28
2,1,1,97.77,163,1.0,100,2023-12-01 12:46:16
2,2,1,223744.1,335987,1.11,100,2023-12-01 12:49:40
2,1,2,85.17,142,1.0,100,2023-12-01 12:53:00
2,2,2,223689.4,335843,1.11,100,2023-12-01 12:56:24
"""
background = """
Cycle,Sample,Repetitions,Count rate (cpm),Counts (reading),Dead time,Real time (s),End time,Live time (s),Counts,Counts uncertainty,Counts uncertainty (%)
1,1,1,83.97,140,1.0,100,2023-11-30 08:44:20,100.0,139.95,11.830046491878212,8.453052155682895
1,1,2,87.57,146,1.0,100,2023-11-30 08:51:04,100.0,145.95,12.080976781701056,8.277476383488219
2,1,1,97.77,163,1.0,100,2023-12-01 12:46:16,100.0,162.95,12.765187033490735,7.833806096036044
2,1,2,85.17,142,1.0,100,2023-12-01 12:53:00,100.0,141.95,11.914277149705725,8.393291405217138
"""
sample = """
Cycle,Sample,Repetitions,Count rate (cpm),Counts (reading),Dead time,Real time (s),End time,Live time (s),Counts,Counts uncertainty,Counts uncertainty (%)
1,2,1,252623.23,374237,1.125,100,2023-11-30 08:47:44,88.88888888888889,374256.63703703706,611.7651812885701,0.16346141143464313
1,2,2,251953.09,373593,1.124,100,2023-11-30 08:54:28,88.9679715302491,373595.9223013048,611.2249359289139,0.1636058906006906
2,2,1,223744.1,335987,1.11,100,2023-12-01 12:49:40,90.09009009009009,335952.1021021021,579.6137525129145,0.1725286875379512
2,2,2,223689.4,335843,1.11,100,2023-12-01 12:56:24,90.09009009009009,335869.96996996994,579.5428974372561,0.17254978094322423
"""
net = """
Elapsed time,Elapsed time (s),Count rate (cpm),Counts,Counts uncertainty,Counts uncertainty (%)
0 days 00:00:00,0.0,252539.26,374116.68703703705,611.8795527201714,0.16355313032577887
0 days 00:06:44,404.0,251865.52,373449.9723013048,611.3443156694146,0.16370179703110896
1 days 04:01:56,100916.0,223646.33000000002,335789.15210210206,579.7543032199951,0.17265426818901866
1 days 04:08:40,101320.0,223604.22999999998,335728.01996996993,579.6653517073191,0.17265921139354673
"""
compilation = """
Background,Background,Background,Background,Background,Background,Background,Background,Background,Background,Background,Background,Sample,Sample,Sample,Sample,Sample,Sample,Sample,Sample,Sample,Sample,Sample,Sample,Net,Net,Net,Net,Net,Net
Cycle,Sample,Repetitions,Count rate (cpm),Counts (reading),Dead time,Real time (s),End time,Live time (s),Counts,Counts uncertainty,Counts uncertainty (%),Cycle,Sample,Repetitions,Count rate (cpm),Counts (reading),Dead time,Real time (s),End time,Live time (s),Counts,Counts uncertainty,Counts uncertainty (%),Elapsed time,Elapsed time (s),Count rate (cpm),Counts,Counts uncertainty,Counts uncertainty (%)
1,1,1,83.97,140,1.0,100,2023-11-30 08:44:20,100.0,139.95,11.830046491878212,8.453052155682895,1,2,1,252623.23,374237,1.125,100,2023-11-30 08:47:44,88.88888888888889,374256.63703703706,611.7651812885701,0.16346141143464313,0 days 00:00:00,0.0,252539.26,374116.68703703705,611.8795527201714,0.16355313032577887
1,1,2,87.57,146,1.0,100,2023-11-30 08:51:04,100.0,145.95,12.080976781701056,8.277476383488219,1,2,2,251953.09,373593,1.124,100,2023-11-30 08:54:28,88.9679715302491,373595.9223013048,611.2249359289139,0.1636058906006906,0 days 00:06:44,404.0,251865.52,373449.9723013048,611.3443156694146,0.16370179703110896
2,1,1,97.77,163,1.0,100,2023-12-01 12:46:16,100.0,162.95,12.765187033490735,7.833806096036044,2,2,1,223744.1,335987,1.11,100,2023-12-01 12:49:40,90.09009009009009,335952.1021021021,579.6137525129145,0.1725286875379512,1 days 04:01:56,100916.0,223646.33000000002,335789.15210210206,579.7543032199951,0.17265426818901866
2,1,2,85.17,142,1.0,100,2023-12-01 12:53:00,100.0,141.95,11.914277149705725,8.393291405217138,2,2,2,223689.4,335843,1.11,100,2023-12-01 12:56:24,90.09009009009009,335869.96996996994,579.5428974372561,0.17254978094322423,1 days 04:08:40,101320.0,223604.22999999998,335728.01996996993,579.6653517073191,0.17265921139354673
"""


class TestHidexTDCRProcessor:
    @pytest.fixture
    def processor(self):
        processor = HidexTDCRProcessor(radionuclide='Lu-177', year=2023, month=11)
        processor.process_readings(input_folder='./data/hidex_tdcr', time_unit='s', save=False)
        return processor

    @pytest.fixture
    def expected_summary(self):
        df = pd.read_csv(StringIO(summary))
        df[df.columns[-1]] = pd.to_datetime(df[df.columns[-1]], format='%Y-%m-%d %H:%M:%S')
        return df

    @pytest.fixture
    def expected_readings(self):
        df = pd.read_csv(StringIO(readings))
        df[df.columns[-1]] = pd.to_datetime(df[df.columns[-1]], format='%Y-%m-%d %H:%M:%S')
        return df

    @pytest.fixture
    def expected_background(self):
        df = pd.read_csv(StringIO(background))
        df[df.columns[7]] = pd.to_datetime(df[df.columns[7]], format='%Y-%m-%d %H:%M:%S')
        return df

    @pytest.fixture
    def expected_sample(self):
        df = pd.read_csv(StringIO(sample))
        df[df.columns[7]] = pd.to_datetime(df[df.columns[7]], format='%Y-%m-%d %H:%M:%S')
        return df

    @pytest.fixture
    def expected_net(self):
        df = pd.read_csv(StringIO(net))
        df[df.columns[0]] = pd.to_timedelta(df[df.columns[0]])
        return df

    @pytest.fixture
    def expected_compilation(self):
        df = pd.read_csv(StringIO(compilation), header=[0, 1])
        df[df.columns[7]] = pd.to_datetime(df[df.columns[7]], format='%Y-%m-%d %H:%M:%S')
        df[df.columns[19]] = pd.to_datetime(df[df.columns[19]], format='%Y-%m-%d %H:%M:%S')
        df[df.columns[24]] = pd.to_timedelta(df[df.columns[24]])
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

    def test_compilation(self, processor, expected_compilation):
        pd.testing.assert_frame_equal(processor.compile_measurements(), expected_compilation)
