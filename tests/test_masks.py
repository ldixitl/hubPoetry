from typing import List, Union

import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "numbers, expected",
    [
        (1234567890123456, "1234 56** **** 3456"),
        (9876543210987654, "9876 54** **** 7654"),
        (1111222233334444, "1111 22** **** 4444"),
        (5555666677778888, "5555 66** **** 8888"),
    ],
)
def test_mask_card_number(numbers: int, expected: str) -> None:
    assert get_mask_card_number(numbers) == expected


@pytest.mark.parametrize("numbers_invalid_type", [None, "1234 5678 9876 5432", "555566a677778888"])
def test_get_mask_card_number_invalid_type(numbers_invalid_type: Union[None, str]) -> None:
    with pytest.raises(TypeError):
        get_mask_card_number(numbers_invalid_type)


@pytest.mark.parametrize("numbers_invalid_value", [98765432109876547, 123456789123456])
def test_get_mask_card_number_invalid_value(numbers_invalid_value: int) -> None:
    with pytest.raises(ValueError):
        get_mask_card_number(numbers_invalid_value)


@pytest.mark.parametrize(
    "numbers, expected",
    [
        (12345678901234567890, "**7890"),
        (98765432109876543210, "**3210"),
        (11112222333344445555, "**5555"),
        (55556666777788889999, "**9999"),
    ],
)
def test_mask_account_number(numbers: int, expected: str) -> None:
    assert get_mask_account(numbers) == expected


@pytest.mark.parametrize("numbers_invalid_type", [None, "11112222333344445555", []])
def test_get_mask_account_invalid_type(numbers_invalid_type: Union[None, str, List]) -> None:
    with pytest.raises(TypeError):
        get_mask_account(numbers_invalid_type)


@pytest.mark.parametrize("numbers_invalid_value", [1234567890123456789, 123456789012345678901])
def test_get_mask_account_invalid_value(numbers_invalid_value: int) -> None:
    with pytest.raises(ValueError):
        get_mask_account(numbers_invalid_value)
