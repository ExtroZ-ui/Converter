from pymongo import MongoClient
from datetime import datetime


class CurrencyConverter:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
        self.db = self.client["currency_db"]
        self.collection = self.db["rates"]

    def _get_rates_by_date(self, date_str: str):
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Неверный формат даты. Используйте YYYY-MM-DD.")

        entry = self.collection.find_one({"date": dt})
        if not entry:
            raise ValueError(f"Нет данных для даты: {date_str}")
        return entry["rates"]

    def _get_latest_rates(self):
        latest_entry = self.collection.find_one(sort=[("date", -1)])
        if not latest_entry:
            raise ValueError("Нет доступных данных о курсах.")
        return latest_entry["rates"]

    def convert(self, from_currency: str, to_currency: str, amount: float, date: str = None) -> float:
        if date:
            rates = self._get_rates_by_date(date)
        else:
            rates = self._get_latest_rates()

        if from_currency not in rates:
            raise ValueError(f"Неподдерживаемый код валюты: {from_currency}")
        if to_currency not in rates:
            raise ValueError(f"Неподдерживаемый код валюты: {to_currency}")

        usd_amount = amount / rates[from_currency]  # Конвертируем
        return usd_amount * rates[to_currency]

    def get_currencies(self):
        rates = self._get_latest_rates()
        return list(rates.keys())

    def get_available_dates(self):
        # Получаем все уникальные даты из коллекции, сортируем их по возрастанию
        dates_cursor = self.collection.find({}, {"date": 1, "_id": 0}).sort("date", 1)
        dates = []
        for doc in dates_cursor:
            if "date" in doc and isinstance(doc["date"], datetime):
                dates.append(doc["date"].strftime("%Y-%m-%d"))
        return dates
