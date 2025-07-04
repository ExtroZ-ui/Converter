# Currency Converter API

**Currency Converter** — это сервис для конвертации валют с REST API и удобной документацией через Swagger UI (OpenAPI).  
Реализован на Python, работает как локально, так и на сервере (может отключится т.к временный).

---

## 🚀 Быстрый старт
Для работы с сервером:
1. UI [https://converter-cpgc.onrender.com](https://converter-cpgc.onrender.com)
2. Swagger [https://extroz-ui.github.io/Converter/swagger_ui.html](https://extroz-ui.github.io/Converter/swagger_ui.html)
   
Для лакального использования:
1. Клонируйте репозиторий и переключитесь на ветку `apispec`:

   ```bash
   git clone -b apispec https://github.com/ExtroZ-ui/Converter.git
   cd Converter
   
2. Запустите сервер:
   
    ```bash
   python server.py

3.Откройте в браузере:

- http://localhost:8000 — главная страница.
- http://localhost:8000/api-docs — Swagger UI с документацией и тестами API.

## 📖 Использование API

| Действие              | URL                                | Метод | Описание                                                                                                   |
| --------------------- |------------------------------------| ----- |------------------------------------------------------------------------------------------------------------|
| Получить список валют | `/currencies`                      | GET   | Возвращает список доступных валют в формате JSON.                                                          |
| Конвертировать сумму  | `/currencies/{from}/{to}?{amount}` | GET  | Валюты передаются в виде path-параметров (`from`, `to`), сумма — в query (`amount`), `date` - опционально. |
| Получить список валют | `/available-dates`                 | GET   | Получить списрк доступных дат курсов валют.                                                                |

## Подробности по GET-запросу /currencies
### Описание
GET /currencies — запрос для получения актуального списка валют, которые поддерживаются сервисом конвертации. Этот список используется для отображения доступных валют в интерфейсах и для проверки корректности параметров при конвертации.

#### Пример запроса /currencies (GET)
Request URL
 - [https://converter-cpgc.onrender.com/currencies](https://converter-cpgc.onrender.com/currencies)  
 - [http://localhost:8000/currencies](http://localhost:8000/currencies)

#### Пример ответа

  ```
[
  "USD",
  "EUR",
  "RUB",
  "JPY",
  "GBP"
]
  ```

## Подробности по GET-запросу /currencies/{from}/{to}?{amount}
### Описание
GET /currencies/{from}/{to}?{amount} — валюты передаются в виде path-параметров (`from`, `to`), сумма — в query (`amount`)
- from — код валюты, из которой конвертируем (например, "USD")
- to — код валюты, в которую конвертируем (например, "EUR")
- amount — сумма в валюте from
  
#### Пример запроса GET /currencies/{from}/{to}?{amount}
  ```
/currencies/RUB/USD?amount=100.5
  ```
#### Пример ответа

  ```
{
"from": "RUB",
"to": "USD",
"amount": 100.5,
 "result": 1.1
}
  ```

## Подробности по GET-запросу /available-dates
### Описание
GET /available-dates — запрос для получения списка дат (`date`)
  
#### Пример запроса GET /available-dates
  ```
/available-dates
  ```
#### Пример ответа

  ```
{
  "2024-01-01",
  "2024-01-02",
  "2024-01-03"
}
  ```

## 📚 Документация API (Swagger UI)
Документация генерируется из спецификации OpenAPI (docs/swagger.yaml).
Swagger UI доступен по адресу:
  - http://localhost:8000/api-docs — локально.
  - https://extroz-ui.github.io/Converter/swagger_ui.html — онлайн.

## 🌐 Конфигурация серверов
В файле docs/swagger.yaml указаны несколько серверов:

  ```
servers:
  - url: http://localhost:8000
    description: Локальный
  - url: https://converter-cpgc.onrender.com
    description: Временный
  ```

## Как использовать Swagger UI
1. Откройте страницу документации по адресу:
 - Локально: [http://localhost:8000/api-docs](http://localhost:8000/api-docs)
 - Веб: [https://extroz-ui.github.io/Converter/swagger_ui.html](https://extroz-ui.github.io/Converter/swagger_ui.html)
2. Выберите нужный эндпоинт в списке слева.
3. Раскройте раздел эндпоинта, чтобы увидеть описание и параметры.
4. Введите необходимые данные (например, для /convert укажите валюты и сумму).
5. Нажмите кнопку Execute — Swagger выполнит запрос и покажет ответ сервера.


## 📖 Тесты
  ```
coverage run -m unittest discover -s tests
coverage report
coverage html
  ```


| File                     | Stmts | Miss | Cover |
|--------------------------|-------|------|--------|
| `converter/__init__.py`  | 0     | 0    | 100%   |
| `converter/converter.py` | 47    | 4    | 91%    |
| `server.py`              | 131   | 33   | 75%    |
| `tests/test_converter.py`| 39    | 2    | 95%    |
| `tests/test_server.py`   | 121   | 3    | 98%    |
| **Total**                | 338   | 42   | **88%** |

