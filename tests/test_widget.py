from typing import Type, Union

import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "data, expected",
    [
        (
            "Счет 12345678901234567890",
            "Счет **7890",
        ),
        (
            "Visa 1234567812345678",
            "Visa 1234 56** **** 5678",
        ),
        (
            "MasterCard 9876543210987654",
            "MasterCard 9876 54** **** 7654",
        ),
    ],
)
def test_mask_account_card_valid(data: str, expected: str) -> None:
    assert mask_account_card(data) == expected


def test_mask_account_card_invalid(invalid_card_number: str, invalid_account_number: str) -> None:
    with pytest.raises(ValueError):
        mask_account_card(invalid_card_number)

    with pytest.raises(ValueError):
        mask_account_card("Visa 5490548934s2548g")

    with pytest.raises(ValueError):
        mask_account_card(invalid_account_number)

    with pytest.raises(TypeError):
        mask_account_card(12346)

    with pytest.raises(ValueError):
        mask_account_card("Счет 54329394302034fhs")


@pytest.mark.parametrize(
    "input_date,expected_output",
    [
        # Проверка правильного преобразования даты
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2000-01-01T00:00:00.000000", "01.01.2000"),
        ("1999-12-31T23:59:59.999999", "31.12.1999"),
    ],
)
def test_get_date_valid(input_date: str, expected_output: str) -> None:
    assert get_date(input_date) == expected_output


def test_get_date_cases(midnight_time: str, end_day_time: str) -> None:
    assert get_date(midnight_time) == "11.03.2024"
    assert get_date(end_day_time) == "11.03.2024"


@pytest.mark.parametrize(
    "input_date,expected_exception",
    [
        # Проверка некорректных входных данных
        ("2024-25-11", ValueError),  # Не соответствует ISO-8601 формату
        ("", ValueError),  # Пустая строка
        ("11.03.2024", ValueError),  # Не соответствует ISO-8601 формату
        (None, TypeError),  # Некорректный тип
        (123456, TypeError),  # Некорректный тип
    ],
)
def test_get_date_invalid(input_date: Union[str, None, int], expected_exception: Type[BaseException]) -> None:
    with pytest.raises(expected_exception):
        get_date(input_date)
