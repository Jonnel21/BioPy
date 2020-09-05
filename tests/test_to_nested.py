import unittest
from src.device.instrument import InstrumentStrategy


class TestToNestedTestCase(unittest.TestCase):
    ''' tests for the to_nested function'''

    def test_to_nested_happy_path(self):
        instrument = InstrumentStrategy()
        test_list = ['F', '1', '2', '3', '4',
                     'A1c', '1', '2', '3', '4',
                     'A1c', '1', '2', '3', '4',
                     'A1c', '1', '2', '3', '4',
                     'A1c', '1', '2', '3', '4', ]

        expected_list = [['F', '1', '2', '3', '4'],
                         ['A1c', '1', '2', '3', '4'],
                         ['A1c', '1', '2', '3', '4'],
                         ['A1c', '1', '2', '3', '4'],
                         ['A1c', '1', '2', '3', '4', ]]

        nested_test_list = instrument.to_nested(test_list)
        self.assertEqual(nested_test_list, expected_list)


if __name__ == '__main__':
    unittest.main()
