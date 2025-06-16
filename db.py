from pymongo import MongoClient
from datetime import datetime, timedelta, timezone
import random

base_currency = "USD"

# Базовые курсы для примера
base_rates = {
    "USD": 1.0,
    "EUR": 0.93,
    "RUB": 91.0,
    "JPY": 155.0,
    "GBP": 0.8
}

def to_mongodb_datetime(date_obj):
    if isinstance(date_obj, datetime):
        dt = date_obj
    else:
        dt = datetime.combine(date_obj, datetime.min.time())
    return dt.replace(tzinfo=timezone.utc)

def apply_daily_variation(base_rates, day_index):
    new_rates = {}
    for curr, rate in base_rates.items():
        # Случайное изменение в диапазоне -15%...+15%
        variation_percent = random.uniform(-0.15, 0.15)
        new_rate = rate * (1 + variation_percent)
        new_rates[curr] = round(new_rate, 4)
    new_rates["USD"] = 1.0  # базовая валюта фиксирована
    return new_rates

try:
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
    client.server_info()

    db = client["currency_db"]
    collection = db["rates"]

    collection.create_index([("date", 1)], unique=True)
    collection.delete_many({})

    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

    rates_data = []
    for i in range(7):
        date = today - timedelta(days=i)
        rates = apply_daily_variation(base_rates, i)
        rates_data.append({
            "date": to_mongodb_datetime(date),
            "base_currency": base_currency,
            "rates": rates
        })

    result = collection.insert_many(rates_data)
    print(f"Успешно загружено {len(result.inserted_ids)} курсов валют в MongoDB за последнюю неделю.")

except Exception as e:
    print(f"Ошибка при работе с MongoDB: {e}")
finally:
    client.close()
