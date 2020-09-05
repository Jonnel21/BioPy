import unittest
from src.device.instrument import InstrumentStrategy as inst


class WrapperDecodeTestCase(unittest.TestCase):
    ''' tests for the wrapper_decode function'''

    def test_wrapper_decode_empty_array(self):
        arr_to_test = []
        self.assertFalse(inst.wrapper_decode(self, arr_to_test))

    def test_wrapper_decode_happy_path(self):
        arr_to_test = [b'one', b'two', b'three']
        expected_result = ['one', 'two', 'three']
        self.assertEqual(expected_result,
                         inst.wrapper_decode(self, arr_to_test))

    def test_wrapper_decode_sad_path(self):
        arr_to_test = [b'one', b'two', b'three']
        expected_result = ['one1', 'two2', 'three3']
        self.assertNotEqual(expected_result,
                            inst.wrapper_decode(self, arr_to_test))


if __name__ == '__main__':
    unittest.main()
