from converter.converter import CurrencyConverter

def main():
    converter = CurrencyConverter()
    amount = 100
    from_currency = "USD"
    to_currency = "EUR"
    result = converter.convert(from_currency, to_currency, amount)
    print(f"{amount} {from_currency} = {result:.2f} {to_currency}")

if __name__ == "__main__":
    main()