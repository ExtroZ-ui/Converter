import unittest
from converter.converter import CurrencyConverter

class TestCurrencyConverter(unittest.TestCase):
    def setUp(self):
        self.converter = CurrencyConverter()


    def test_valid_conversion(self):
        # Проверяем конвертацию по последним курсам
        result = self.converter.convert("USD", "EUR", 100)
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0)

    def test_same_currency(self):
        # Конвертация из валюты в ту же валюту должна вернуть то же число
        amount = 123.45
        result = self.converter.convert("USD", "USD", amount)
        self.assertAlmostEqual(result, amount, places=5)

    def test_invalid_from_currency(self):
        # Проверяем, что при неверном from_currency выбрасывается ValueError
        with self.assertRaises(ValueError):
            self.converter.convert("XXX", "USD", 100)

    def test_invalid_to_currency(self):
        # Проверяем, что при неверном to_currency выбрасывается ValueError
        with self.assertRaises(ValueError):
            self.converter.convert("USD", "ZZZ", 100)

    def test_conversion_with_date(self):
        # Если есть даты, тестируем конвертацию по дате
        dates = self.converter.get_available_dates()
        if dates:
            date = dates[0]
            result = self.converter.convert("USD", "EUR", 100, date=date)
            self.assertIsInstance(result, float)
            self.assertGreater(result, 0)
        else:
            self.skipTest("Нет доступных дат для тестирования с датой")

    def test_get_currencies(self):
        # Проверяем, что список валют не пустой и содержит USD
        currencies = self.converter.get_currencies()
        self.assertIsInstance(currencies, list)
        self.assertIn("USD", currencies)

    def test_get_available_dates(self):
        # Проверяем, что даты возвращаются в виде списка строк в нужном формате
        dates = self.converter.get_available_dates()
        self.assertIsInstance(dates, list)
        for d in dates:
            self.assertIsInstance(d, str)
            self.assertRegex(d, r"\d{4}-\d{2}-\d{2}")

if __name__ == '__main__':
    unittest.main()
