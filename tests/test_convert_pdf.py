import unittest
import os
from src.device.instrument import InstrumentStrategy


class ConvertPdfTestCase(unittest.TestCase):
    ''' tests the convert_pdf function'''

    def test_convert_pdf_one(self):
        instrumet = InstrumentStrategy()
        pdf = ('D:/a/BioPy/BioPy/pdf/d10/19BMTA2306_9-9-3-2-2020-RA1.pdf',)  # build
        # pdf = ('C:/Users/Jonnel/Documents/BioPy/pdf/d10/19BMTA2306_9-9-3-2-2020-RA1.pdf',)  # local
        instrumet.convert_pdf(pdf)
        self.assertTrue(os.path.isdir(instrumet.temp_dir))


if __name__ == '__main__':
    unittest.main()
