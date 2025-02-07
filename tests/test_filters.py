from typing import Dict, List

import pytest

from src.filters import count_transactions_by_category, filter_transactions_by_description


def test_filter_by_description_valid(transactions_list: List[Dict]) -> None:
    assert filter_transactions_by_description(transactions_list, "организ") == [
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
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
    ]

    assert filter_transactions_by_description(transactions_list, "карты") == [
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        }
    ]

    assert filter_transactions_by_description(transactions_list, "") == transactions_list


def test_filter_by_description_empty(transactions_list: List[Dict]) -> None:
    assert filter_transactions_by_description(transactions_list, "пополнение") == []


def test_filter_by_description_invalid() -> None:
    with pytest.raises(TypeError):
        filter_transactions_by_description(
            [
                {
                    "id": 895315941,
                    "state": "EXECUTED",
                    "date": "2018-08-19T04:27:37.904916",
                    "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
                    "description": 54,
                    "from": "Visa Classic 6831982476737658",
                    "to": "Visa Platinum 8990922113665229",
                }
            ],
            "счет",
        )

    with pytest.raises(TypeError):
        filter_transactions_by_description(
            None,
            "счет",
        )

    with pytest.raises(TypeError):
        filter_transactions_by_description(
            [
                {
                    "id": 895315941,
                    "state": "EXECUTED",
                    "date": "2018-08-19T04:27:37.904916",
                    "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
                    "description": "Перевод со счета",
                    "from": "Visa Classic 6831982476737658",
                    "to": "Visa Platinum 8990922113665229",
                }
            ],
            543,
        )


def test_filter_by_description_empty_list() -> None:
    assert filter_transactions_by_description([], "счет") == []


def test_count_transactions_by_category(transactions_list: List[Dict]) -> None:
    categories = ["Перевод организации", "Перевод со счета на счет", "Перевод с карты на карту"]
    assert count_transactions_by_category(transactions_list, categories) == {
        "перевод с карты на карту": 1,
        "перевод со счета на счет": 2,
        "перевод организации": 2,
    }


def test_count_transactions_empty(transactions_list: List[Dict]) -> None:
    assert count_transactions_by_category([], ["перевод"]) == {}
    assert count_transactions_by_category(transactions_list, []) == {}


def test_count_transactions_invalid_types(transactions_list: List[Dict]) -> None:
    with pytest.raises(TypeError):
        count_transactions_by_category("не список", ["перевод"])

    with pytest.raises(TypeError):
        count_transactions_by_category([{"id": 1, "description": 123}], ["перевод"])

    with pytest.raises(TypeError):
        count_transactions_by_category(transactions_list, "перевод")
