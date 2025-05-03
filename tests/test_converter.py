import unittest
from converter.converter import CurrencyConverter

class TestCurrencyConverter(unittest.TestCase):

    def setUp(self):
        self.converter = CurrencyConverter()

    def test_usd_to_eur(self):
        self.assertAlmostEqual(self.converter.convert("USD", "EUR", 100), 93.0, places=2)

    def test_invalid_currency(self):
        with self.assertRaises(ValueError):
            self.converter.convert("USD", "XYZ", 100)

    def test_same_currency(self):
        self.assertEqual(self.converter.convert("USD", "USD", 100), 100)