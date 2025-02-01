from unittest.mock import patch

import pandas as pd
import pytest

from src.transaction_parser import parse_transaction_auto


@pytest.fixture
def sample_transactions() -> list:
    return [
        {
            "id": 650703,
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": 16210,
            "currency_name": "Sol",
            "currency_code": "PEN",
            "from": "Счет 58803664561298323391",
            "to": "Счет 39745660563456619397",
            "description": "Перевод организации",
        }
    ]


@patch("pandas.read_csv")
def test_parse_transactions_auto_csv(mock_read_csv, sample_transactions) -> None:
    """Тестирование чтения CSV-файлов"""
    df_mock = pd.DataFrame(sample_transactions)
    mock_read_csv.return_value = df_mock

    transactions = parse_transaction_auto("data/transactions.csv")

    assert transactions == sample_transactions
    mock_read_csv.assert_called_once_with("data/transactions.csv", sep=";")


@patch("pandas.read_excel")
def test_parse_transactions_auto_xlsx(mock_read_excel, sample_transactions) -> None:
    """Тестирование чтения XLSX-файлов"""
    df_mock = pd.DataFrame(sample_transactions)
    mock_read_excel.return_value = df_mock

    transactions = parse_transaction_auto("data/transactions.xlsx")

    assert transactions == sample_transactions
    mock_read_excel.assert_called_once_with("data/transactions.xlsx")


def test_parse_transactions_auto_unsupported_format() -> None:
    """Тестирование ошибки при неподдерживаемом формате"""
    transactions = parse_transaction_auto("data/transactions.txt")
    assert transactions == []


def test_parse_transactions_auto_file_not_found() -> None:
    """Тестирование ошибки при отсутствии файла"""
    with patch("pandas.read_csv", side_effect=FileNotFoundError):
        transactions = parse_transaction_auto("data/missing.csv")
        assert transactions == []


@patch("pandas.read_excel")
def test_parse_transactions_auto_empty_file(mock_read_excel) -> None:
    """Тестирование ошибки при пустом файле"""
    df_mock = pd.DataFrame()
    mock_read_excel.return_value = df_mock

    transactions = parse_transaction_auto("data/empty.xlsx")

    assert transactions == []
    mock_read_excel.assert_called_once_with("data/empty.xlsx")
