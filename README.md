# Проект *Bank Operation Hub*

## Описание:

Проект Bank Operation Hub представляет собой виджет банковских операций клиента. 
Он позволяет фильтровать и сортировать операции по различным параметрам. 
А также создавать маски счетов и номеров карт.

### Реализованные функции:
- **Маскирование номеров карт**  
  Реализована функция, которая принимает на вход номер карты и возвращает ее маску.  
  Номер карты замаскирован и отображается в формате `XXXX XX** **** XXXX`, где `X` — цифра номера.
- **Маскирование номеров счетов**  
  Реализована функция, которая принимает на вход номер счета и возвращает его маску.  
  Номер счета замаскирован и отображается в формате `**XXXX`, где `X` — цифра номера.
- **Маскирование по типу**  
  Реализована функция, которая принимает один аргумент — строку, содержащую тип и номер карты или счета, и возвращает 
строку с замаскированным номером. Для карт и счетов используется разный тип маскировки.
- **Форматирование дат**  
  Реализована функция, которая принимает строку с датой в формате `"2024-03-11T02:26:18.671407"` и возвращает дату 
в формате `"ДД.ММ.ГГГГ"` (`"11.03.2024"`).
- **Фильтрация по состоянию операций**  
  Функция принимает список словарей и опционально значение для ключа `state` (по умолчанию `'EXECUTED'`). 
Возвращается новый список словарей, содержащий только те элементы, у которых ключ `state` соответствует указанному 
значению.
- **Сортировка по дате**  
  Функция принимает список словарей и необязательный параметр, задающий порядок сортировки (по умолчанию — убывание). 
Возвращается новый список, отсортированный по ключу `date`.
- **Загрузка транзакций из файла**  
  Функция `load_transactions` принимает путь до JSON-файла и возвращает список словарей с данными о финансовых
транзакциях.
- **Конвертация суммы транзакции в рубли**  
  Функция `currency_exchanger` принимает транзакцию (словарь) и возвращает сумму транзакции в рублях 
(тип данных — `float`).  
Для работы функции `currency_exchanger` необходимо указать API-ключ в файле `.env` по инструкции из
[**.env.sample**](.env.sample).

### Реализованные генераторы:
- **Фильтрация транзакций по валюте**  
  Функция `filter_by_currency` принимает список транзакций и возвращает итератор, который поочередно выдает 
транзакции, где валюта соответствует заданной (например, `'USD'`).
- **Описание транзакций**  
  Генератор `transaction_descriptions` принимает список транзакций и возвращает описание каждой по очереди. 
- **Генерация номеров банковских карт**  
  Генератор `card_number_generator` принимает начальное и конечное значение диапазона и генерирует номера 
банковских карт в формате `XXXX XXXX XXXX XXXX`.  

### Реализованные декораторы:
- **Логгер**  
  Декоратор `logger` логирует начало и конец выполнения функции, а также ее результат или возникшие ошибки. 
Он принимает необязательный параметр `filename`, который определяет, куда будут записываться логи (в файл или в консоль). В случае успешного выполнения функции логируются имя функции, входные параметры, результат и время выполнения. В случае ошибки записываются тип ошибки и сообщение об исключении, а также входные параметры.

## Установка:

1. Клонируйте репозиторий:
```
git clone https://github.com/ldixitl/bankOperationHub.git
```
2. Установите зависимости:

Используется Poetry для управления зависимостями. Убедитесь, что Poetry установлен.
После установки выполните:
```
poetry install
```

## Использование:
### Пример работы функций:
1. **Маскировка номера карты**
   ```python
   from src.masks import get_mask_card_number

   card_number = 1234567812345678
   print(get_mask_card_number(card_number))
   # Вывод: 1234 56** **** 5678
   ```

2. **Маскировка номера счета**
   ```python
   from src.masks import get_mask_account

   account_number = 987654321
   print(get_mask_account(account_number))
   # Вывод: **4321
   ```

3. **Фильтрация операций**
   ```python
   from src.processing import filter_by_state

   operations = [
       {"id": 1, "state": "EXECUTED", "date": "2023-12-01"},
       {"id": 2, "state": "CANCELED", "date": "2023-11-01"}
   ]
   print(filter_by_state(operations, state="CANCELED"))
   # Вывод: [{'id': 2, 'state': 'CANCELED', 'date': '2023-11-01'}]
   ```

4. **Сортировка операций**
   ```python
   from src.processing import sort_by_date

   operations = [
       {"id": 1, "date": "2023-12-01", "amount": 100},
       {"id": 2, "date": "2023-11-01", "amount": 200}
   ]
   print(sort_by_date(operations, if_reverse=False))
   # Вывод: [{'id': 2, 'date': '2023-11-01', 'amount': 200},
   #          {'id': 1, 'date': '2023-12-01', 'amount': 100}]
   ```
   
5. **Загрузка транзакций из файла**
```python
from src.utils import load_transactions

file_path = "data/operations.json"
transactions = load_transactions(file_path)
print(transactions)
# Вывод: [{'id': 1, 'amount': '500.00', 'currency': {'code': 'USD'}}, ...]
```

6. **Конвертация суммы транзакции в рубли**
```python
from src.external_api import currency_exchanger

transaction = {
    "operationAmount": {
        "amount": "100.00",
        "currency": {"code": "USD"}
    }
}
converted_amount = currency_exchanger(transaction)
print(converted_amount)
# Вывод: 7545.00 (в зависимости от курса валют)
```

### Пример работы генераторов:

1. **Фильтрация транзакций по валюте**  
   ```python
   from src.generators import filter_by_currency

   transactions = [
       {
           "id": 1,
           "operationAmount": {
               "amount": "500.00",
               "currency": {"code": "USD", "name": "Dollar"}
           },
           "description": "Payment"
       },
       {
           "id": 2,
           "operationAmount": {
               "amount": "300.00",
               "currency": {"code": "EUR", "name": "Euro"}
           },
           "description": "Refund"
       }
   ]

   usd_transactions = filter_by_currency(transactions, "USD")
   print(next(usd_transactions))
   # Вывод: {'id': 1, 'operationAmount': {'amount': '500.00', 'currency': {'code': 'USD', 'name': 'Dollar'}}, 'description': 'Payment'}
   ```

2. **Описание транзакций**  
   ```python
   from src.generators import transaction_descriptions

   transactions = [
       {"id": 1, "description": "Payment"},
       {"id": 2, "description": "Refund"},
       {"id": 3, "description": "Transfer"}
   ]

   descriptions = transaction_descriptions(transactions)
   print(next(descriptions))
   # Вывод: Payment
   print(next(descriptions))
   # Вывод: Refund
   ```

3. **Генерация номеров банковских карт**  
   ```python
   from src.generators import card_number_generator

   for card in card_number_generator(1, 3):
       print(card)
   # Вывод:
   # 0000 0000 0000 0001
   # 0000 0000 0000 0002
   # 0000 0000 0000 0003
   ```

### Пример работы декораторов:
  1. **Логгер**
  ```python
  from src.decorators import logger
  @logger(filename="my_log.txt")
  def add(x, y):
      return x + y
  ```

  В случае успешного выполнения:
  ```
  Function start: Sun Jan 12 21:50:12 2025
  Function 'add' called with args: (1, 2) and kwargs: {}.
  Result: 3
  Function finish: Sun Jan 12 21:50:12 2025
  ```

  В случае ошибки:
  ```
  Function start: Sun Jan 12 21:50:12 2025
  The function 'add' failed with an error 'ZeroDivisionError: division by zero'
  Inputs - args: (1, 0) and kwargs: {}
  ```

## Тестирование

Для тестирования в проекте используются **pytest** и плагин **pytest-cov** для измерения покрытия кода тестами.

### Запуск тестов
Чтобы запустить тесты, выполните команду:
```bash
pytest
```

### Отчёт о покрытии кода
Для генерации отчёта о покрытии кода в формате HTML выполните:

```bash
pytest --cov=src --cov-report=html
```
После выполнения команда сгенерирует папку **htmlcov**, содержащую отчёт. 
Откройте файл **htmlcov/index.html** в браузере, чтобы просмотреть детализированный отчёт.

## Лицензия:

Этот проект лицензирован по [лицензии MIT](LICENSE).
