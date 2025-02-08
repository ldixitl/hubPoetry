from typing import Dict, List, Type, Union

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


def test_filter_by_currency_corrected(transactions_list: List[Dict], usd_transactions: List[Dict]) -> None:
    assert list(filter_by_currency(transactions_list, "USD")) == usd_transactions
    assert list(filter_by_currency(transactions_list, "CNY")) == []


def test_filter_by_currency_empty(transactions_list: List[Dict]) -> None:
    assert list(filter_by_currency([], "USD")) == []


def test_filter_by_currency_invalid_format() -> None:
    with pytest.raises(TypeError):
        next(filter_by_currency(None, "USD"))


def test_transaction_descriptions_corrected(transactions_list: List[Dict]) -> None:
    descriptions = transaction_descriptions(transactions_list)
    assert next(descriptions) == "Перевод организации"
    assert next(descriptions) == "Перевод со счета на счет"
    assert next(descriptions) == "Перевод со счета на счет"
    assert next(descriptions) == "Перевод с карты на карту"
    assert next(descriptions) == "Перевод организации"


def test_transactions_descriptions_empty() -> None:
    assert list(transaction_descriptions([])) == []


def test_transactions_descriptions_invalid_format() -> None:
    with pytest.raises(TypeError):
        next(transaction_descriptions(None))


def test_transactions_descriptions_invalid_key() -> None:
    with pytest.raises(KeyError):
        list(
            transaction_descriptions(
                [
                    {
                        "id": 939719570,
                        "state": "EXECUTED",
                        "date": "2018-06-30T02:08:58.425572",
                        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
                        "description": "Перевод организации",
                        "from": "Счет 75106830613657916952",
                        "to": "Счет 11776614605963066702",
                    },
                    {
                        "id": 142264268,
                        "state": "EXECUTED",
                        "date": "2019-04-04T23:20:05.206878",
                        "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
                        "from": "Счет 19708645243227258542",
                        "to": "Счет 75651667383060284188",
                    },
                ]
            )
        )


def test_card_number_generator_corrected() -> None:
    card_numbers = list(card_number_generator(1, 5))
    assert card_numbers == [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005",
    ]


@pytest.mark.parametrize(
    "input_start, input_stop, expected_exception",
    [
        # Проверка некорректных входных данных
        (None, 12, TypeError),  # Некорректный тип
        (123456, "1234567", TypeError),  # Некорректный тип
        (11, 10, ValueError),  # start > stop
    ],
)
def test_card_number_generator_invalid_format(
    input_start: Union[None, int], input_stop: Union[int, str], expected_exception: Type[BaseException]
) -> None:
    with pytest.raises(expected_exception):
        next(card_number_generator(input_start, input_stop))
