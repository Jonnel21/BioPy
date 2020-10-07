import unittest
from src.device.instrument import InstrumentStrategy


class SortHeadersTestCase(unittest.TestCase):
    ''' tests the sort_headers function'''

    def test_sample(self):
        instrument = InstrumentStrategy()
        param = 'Sample'
        expected_result = 0
        test_result = instrument.sort_headers(param)
        self.assertEqual(test_result, expected_result)

    def test_date(self):
        instrument = InstrumentStrategy()
        param = 'Date'
        expected_result = 0
        test_result = instrument.sort_headers(param)
        self.assertEqual(test_result, expected_result)

    def test_time(self):
        instrument = InstrumentStrategy()
        param = 'Time'
        expected_result = 0
        test_result = instrument.sort_headers(param)
        self.assertEqual(test_result, expected_result)

    def test_injection(self):
        instrument = InstrumentStrategy()
        param = 'Inj'
        expected_result = 0
        test_result = instrument.sort_headers(param)
        self.assertEqual(test_result, expected_result)

    def test_rack(self):
        instrument = InstrumentStrategy()
        param = 'Rack'
        expected_result = 0
        test_result = instrument.sort_headers(param)
        self.assertEqual(test_result, expected_result)

    def test_total_hb_area(self):
        instrument = InstrumentStrategy()
        param = 'Total Hb Area'
        expected_result = 0
        test_result = instrument.sort_headers(param)
        self.assertEqual(test_result, expected_result)

    def test_pattern(self):
        instrument = InstrumentStrategy()
        param = 'Pattern'
        expected_result = 0
        test_result = instrument.sort_headers(param)
        self.assertEqual(test_result, expected_result)

    def test_well(self):
        instrument = InstrumentStrategy()
        param = 'Well'
        expected_result = 0
        test_result = instrument.sort_headers(param)
        self.assertEqual(test_result, expected_result)

    def test_plate(self):
        instrument = InstrumentStrategy()
        param = 'Plate'
        expected_result = 0
        test_result = instrument.sort_headers(param)
        self.assertEqual(test_result, expected_result)

    def test_tube(self):
        instrument = InstrumentStrategy()
        param = 'Tube'
        expected_result = 0
        test_result = instrument.sort_headers(param)
        self.assertEqual(test_result, expected_result)

    def test_run(self):
        instrument = InstrumentStrategy()
        param = 'Run'
        expected_result = 0
        test_result = instrument.sort_headers(param)
        self.assertEqual(test_result, expected_result)

    def test_lotnum(self):
        instrument = InstrumentStrategy()
        param = 'Lot #'
        expected_result = 0
        test_result = instrument.sort_headers(param)
        self.assertEqual(test_result, expected_result)

    def test_lotid(self):
        instrument = InstrumentStrategy()
        param = 'Lot ID'
        expected_result = 0
        test_result = instrument.sort_headers(param)
        self.assertEqual(test_result, expected_result)

    def test_expiration_date(self):
        instrument = InstrumentStrategy()
        param = 'Expiration Date'
        expected_result = 0
        test_result = instrument.sort_headers(param)
        self.assertEqual(test_result, expected_result)

    def test_unknown(self):
        instrument = InstrumentStrategy()
        unknown = 'Unknown1'
        expected_result = 2
        test_result = instrument.sort_headers(unknown)
        self.assertEqual(test_result, expected_result)

    def test_unknown_no_digit(self):
        instrument = InstrumentStrategy()
        unknown = 'Unknown'
        expected_result = 1
        test_result = instrument.sort_headers(unknown)
        self.assertEqual(test_result, expected_result)

    def test_other(self):
        instrument = InstrumentStrategy()
        param = 'Peak'
        expected_result = 1
        test_result = instrument.sort_headers(param)
        self.assertEqual(test_result, expected_result)


if __name__ == '__main__':
    unittest.main()
