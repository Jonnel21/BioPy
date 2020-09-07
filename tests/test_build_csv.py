import unittest
import os
from src.device.instrument import InstrumentStrategy
from src.d10 import D10Strategy


class BuildCsvTestCase(unittest.TestCase):
    ''' tests the build_csv function'''

    def test_csv_file(self):
        instrument = InstrumentStrategy()
        d10 = D10Strategy()
        pdf = ('../pdf/d10/19BMTA2306_9-9-3-2-2020-RA1.pdf',)
        save = os.path.join(os.getenv('programdata'), 'test.csv')
        instrument.convert_pdf(pdf)
        d10.build_csv(save)
        self.assertTrue(os.path.isfile(save))


if __name__ == '__main__':
    unittest.main()
