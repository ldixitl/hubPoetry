import os
from unittest.mock import patch

import pytest

from src.external_api import currency_exchanger


@patch("src.external_api.requests.get")
def test_currency_exchanger_success(mock_get) -> None:
    """Тест успешной конвертации валюты"""
    mock_response = {"result": 7500.50}
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    transaction = {"operationAmount": {"amount": "100", "currency": {"code": "USD"}}}
    result = currency_exchanger(transaction)
    assert result == 7500.50
    mock_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/convert",
        headers={"apikey": os.getenv("API_KEY_EXCHANGER")},
        params={"to": "RUB", "from": "USD", "amount": "100"},
    )


@patch("src.external_api.requests.get")
def test_currency_exchanger_rub_currency(mock_get) -> None:
    """Тест, когда валюта уже в рублях"""
    transaction = {"operationAmount": {"amount": "100", "currency": {"code": "RUB"}}}
    result = currency_exchanger(transaction)
    assert result == 100.0
    mock_get.assert_not_called()


@patch("src.external_api.requests.get")
def test_currency_exchanger_missing_result_key(mock_get) -> None:
    """Тест обработки отсутствия ключа 'result' в ответе API"""
    mock_response = {}
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    transaction = {"operationAmount": {"amount": "100", "currency": {"code": "USD"}}}
    with pytest.raises(Exception):
        currency_exchanger(transaction)


def test_currency_exchanger_api_key_not_set() -> None:
    """Тест обработки отсутствия API ключа"""
    with patch("src.external_api.API_KEY_EXCHANGER", None):
        transaction = {"operationAmount": {"amount": "100", "currency": {"code": "USD"}}}
        with pytest.raises(ValueError):
            currency_exchanger(transaction)
