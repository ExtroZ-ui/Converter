import unittest
from converter.converter import CurrencyConverter

class TestCurrencyConverter(unittest.TestCase):
    def setUp(self):
        self.converter = CurrencyConverter()

    def test_valid_conversion(self):
        result = self.converter.convert("USD", "EUR", 100)
        self.assertIsInstance(result, float)

    def test_same_currency(self):
        result = self.converter.convert("USD", "USD", 100)
        self.assertAlmostEqual(result, 100)

    def test_invalid_from_currency(self):
        with self.assertRaises(ValueError):
            self.converter.convert("XXX", "USD", 100)

    def test_invalid_to_currency(self):
        with self.assertRaises(ValueError):
            self.converter.convert("USD", "ZZZ", 100)

if __name__ == '__main__':
    unittest.main()