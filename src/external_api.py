import os

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY_EXCHANGER = os.getenv("API_KEY_EXCHANGER")
URL_EXCHANGER = "https://api.apilayer.com/exchangerates_data/convert"


def currency_exchanger(transaction: dict) -> float:
    """Принимает транзакцию и конвертирует сумму в рубли"""
    amount = transaction["operationAmount"]["amount"]
    currency = transaction["operationAmount"]["currency"]["code"]

    if currency == "RUB":
        return float(amount)

    if not API_KEY_EXCHANGER:
        raise ValueError("API_KEY_EXCHANGER is not set.")

    payload = {"to": "RUB", "from": currency, "amount": amount}
    headers = {"apikey": API_KEY_EXCHANGER}

    try:
        response = requests.get(URL_EXCHANGER, headers=headers, params=payload)
        response.raise_for_status()

        data = response.json()
        if "result" in data:
            rate = data["result"]
            return round(rate, 2)
        else:
            raise KeyError("Ключ 'result' отсутствует в ответе API.")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Ошибка при выполнении запроса: {e}")
    except KeyError as e:
        # Обработка отсутствия ключа 'result'
        raise Exception(f"Ошибка в структуре ответа API: {e}")
