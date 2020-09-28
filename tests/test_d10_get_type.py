import unittest
from src.d10 import D10Strategy
from src.variant2 import VariantStrategy
from src.nbs import NbsStrategy


class GetTypeTestCase(unittest.TestCase):
    ''' tests the get_type function'''

    def test_get_type_d10(self):
        d10 = D10Strategy()
        self.assertEqual(d10.get_type(), "D-10")

    def test_get_type_d10_variant(self):
        d10 = D10Strategy()
        variant = VariantStrategy()
        self.assertNotEqual(d10.get_type(), variant.get_type())

    def test_get_type_d10_nbs(self):
        d10 = D10Strategy()
        vnbs = NbsStrategy()
        self.assertNotEqual(d10.get_type(), vnbs.get_type())


if __name__ == '__main__':
    unittest.main()
