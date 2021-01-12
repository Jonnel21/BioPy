import unittest
import os
# import configparser
# from playground.Scripts import chkcsv
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

    # Planning testing infastructure by validating csv file...
    # def test_valid_csv(self):
    #     config = configparser.ConfigParser()
    #     config['Date'] = {'column_required': True, 'data_required': True, 'type': 'integer'}
    #     config['Inj #'] = {'column_required': True, 'data_required': True, 'type': 'integer'}
    #     # config = ['Date', 'Inj #']
    #     # newChkCsv = chkcsv.CsvChecker(config, 'Date Bad', True, False, 0)
    #     # self.assertTrue(newChkCsv)
    #     save = os.path.join(os.getenv('programdata'), 'test.csv')
    #     self.assertTrue(chkcsv.check_csv_file(save, config, False, False, False, False))


if __name__ == '__main__':
    unittest.main()
