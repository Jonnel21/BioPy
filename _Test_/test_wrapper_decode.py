import unittest
from ..instrument import InstrumentStrategy as inst

class WrapperDecodeTestCase(unittest.TestCase):
    ''' tests for the wrapper_decode function'''

    def test_wrapper_decode_empty_array(self):
        arr_to_test = []
        self.assertFalse(instrument.wrapper_decode(self, arr_to_test))

if __name__ == '__main__':
    unittest.main()