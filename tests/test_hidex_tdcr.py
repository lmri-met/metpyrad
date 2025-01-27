import pytest

from metpyrad.hidex_tdcr import HidexTDCRProcessor


@pytest.fixture
def processor():
    processor = HidexTDCRProcessor(radionuclide='Lu-177', year=2023, month=11)
    processor.process_readings(folder_path='./data/hidex_tdcr', time_unit='s', save=False)
    return processor


class TestHidexTDCRProcessor:
    def test_non_dataframe_attributes(self, processor):
        assert processor.radionuclide == 'Lu-177'
        assert processor.year == 2023
        assert processor.month == 11
        assert processor.cycles == 2
        assert processor.cycle_repetitions == 2
        assert processor.repetition_time == 100
        assert processor.measurements == 4
        assert processor.measurement_time == 400
