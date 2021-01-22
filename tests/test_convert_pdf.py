import unittest
import os
from src.device.instrument import InstrumentStrategy


class ConvertPdfTestCase(unittest.TestCase):
    ''' tests the convert_pdf function'''

    def test_directory(self):
        instrumet = InstrumentStrategy()
        pdf = ('../pdf/d10/patient/5.00/19BMTA2306_9-9-3-2-2020-RA1.pdf',)
        instrumet.convert_pdf(pdf)
        self.assertTrue(os.path.isdir(instrumet.temp_dir))

    def test_txt_file(self):
        instrument = InstrumentStrategy()
        pdf = ('../pdf/d10/patient/5.00/19BMTA2306_9-9-3-2-2020-RA1.pdf',)
        instrument.convert_pdf(pdf)
        self.assertTrue(os.path.isfile(os.path.join(instrument.temp_dir,
                                                    '19BMTA2306_9-9-3-2-2020-RA1.txt')))

    def test_file_size_is_empty(self):
        instrument = InstrumentStrategy()
        path_file = os.path.join(instrument.temp_dir,
                                 '19BMTA2306_9-9-3-2-2020-RA1.txt')
        pdf = ('../pdf/d10/patient/5.00/19BMTA2306_9-9-3-2-2020-RA1.pdf',)
        instrument.convert_pdf(pdf)
        self.assertNotEqual(os.stat(path_file).st_size, 0)

    def test_file_size_partially_empty(self):
        instrument = InstrumentStrategy()
        path_file = os.path.join(instrument.temp_dir,
                                 '19BMTA2306_9-9-3-2-2020-RA1.txt')
        pdf = ('../pdf/d10/patient/5.00/19BMTA2306_9-9-3-2-2020-RA1.pdf',)
        instrument.convert_pdf(pdf)
        self.assertLess(200, os.stat(path_file).st_size)


if __name__ == '__main__':
    unittest.main()
