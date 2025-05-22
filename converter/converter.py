from converter.currencies import EXCHANGE_CURRENCIES

class CurrencyConverter:
    def convert(self, from_currency: str, to_currency: str, amount: float) -> float:
        if from_currency not in EXCHANGE_CURRENCIES or to_currency not in EXCHANGE_CURRENCIES:
            raise ValueError("Unsupported currency code.")
        usd = amount / EXCHANGE_CURRENCIES[from_currency]
        return usd * EXCHANGE_CURRENCIES[to_currency]

    def get_currencies(self):
        return list(EXCHANGE_CURRENCIES.keys())