from converter.rates import EXCHANGE_RATES

class CurrencyConverter:
    def convert(self, from_currency: str, to_currency: str, amount: float) -> float:
        if from_currency not in EXCHANGE_RATES or to_currency not in EXCHANGE_RATES:
            raise ValueError("Unsupported currency code.")
        usd = amount / EXCHANGE_RATES[from_currency]
        return usd * EXCHANGE_RATES[to_currency]

    def get_currencies(self):
        return list(EXCHANGE_RATES.keys())