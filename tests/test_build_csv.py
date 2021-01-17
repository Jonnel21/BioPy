import unittest
import os
# import configparser
# from playground.Scripts import chkcsv
from src.device.instrument import InstrumentStrategy
from src.d10 import D10Strategy
from src.variant2 import VariantStrategy
from src.nbs import NbsStrategy


class BuildCsvTestCase(unittest.TestCase):
    ''' tests the build_csv function'''

    def setUp(self):
        # initialize parsing algorithms
        self.instrument = InstrumentStrategy()
        self.d10 = D10Strategy()
        self.variant = VariantStrategy()
        self.nbs = NbsStrategy()

        # initialize pdf directories
        self.d10_dir = '../pdf/d10/'
        self.variant_dir = '../pdf/variant/'
        self.vnbs_dir = '../pdf/vnbs/'

        # initialize save directory
        self.save_dir = os.path.abspath(os.getenv('programdata'))

    def test_csv_file(self):
        save = os.path.join(self.save_dir, 'one_entry.csv')
        self.instrument.convert_pdf_test(self.d10_dir)
        self.d10.build_csv(save)
        self.assertTrue(os.path.isfile(save))

    # @unittest.skip('Skipping...')
    def test_d10_50(self):
        save = os.path.join(self.save_dir, 'patient_D10_5.0.csv')
        self.instrument.convert_pdf_test(self.d10_dir)
        self.d10.build_csv(save)
        self.assertTrue(os.path.isfile(save))

    # @unittest.skip('Skipping...')
    def test_variant(self):
        save = os.path.join(self.save_dir, 'patient_variant.csv')
        self.instrument.convert_pdf_test(self.variant_dir)
        self.variant.build_csv(save)
        self.assertTrue(os.path.isfile(save))

    # @unittest.skip('Skipping...')
    def test_vnbs(self):
        save = os.path.join(self.save_dir, 'patient_vnbs.csv')
        self.instrument.convert_pdf_test(self.vnbs_dir)
        self.nbs.build_csv(save)
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
