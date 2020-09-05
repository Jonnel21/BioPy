import unittest
from src.device.instrument import InstrumentStrategy as inst


class RenameUnknownTestCase(unittest.TestCase):
    ''' tests the rename_unknown function'''

    def test_rename_unknown_happy_path(self):
        test_list = ['Jonnel', 'Unknown', 'one']
        expected_result = ['Jonnel', 'Unknown1', 'one']
        inst.rename_unknown(self, test_list)
        self.assertEqual(test_list, expected_result)

    def test_rename_unknown_multiple_unknowns(self):
        test_list = ['Unknown', 'F', 'Unknown', 'A1c', 'Unknown']
        expected_result = ['Unknown1', 'F', 'Unknown2', 'A1c', 'Unknown3']
        inst.rename_unknown(self, test_list)
        self.assertEqual(test_list, expected_result)

    def test_rename_unknown_empty_list(self):
        test_list = []
        expected_result = 'List is empty.'
        self.assertEqual(inst.rename_unknown(self, test_list), expected_result)

    def test_rename_unknown_no_unknowns(self):
        test_list = ['F', 'A1c', 'S', 'E', 'LA1c']
        expected_result = 'There are no Unknowns in the list.'
        self.assertEqual(inst.rename_unknown(self, test_list), expected_result)


if __name__ == '__main__':
    unittest.main()
