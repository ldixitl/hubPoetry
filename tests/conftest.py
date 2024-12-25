from typing import Dict, List

import pytest


@pytest.fixture
def operations_list() -> List[Dict]:
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.fixture
def invalid_card_number() -> str:
    return "123456789012"  # Номер слишком короткий


@pytest.fixture
def invalid_account_number() -> str:
    return "Счет 1234567"  # Номер слишком короткий


@pytest.fixture
def midnight_time() -> str:
    return "2024-03-11T00:00:00.000000"


@pytest.fixture
def end_day_time() -> str:
    return "2024-03-11T23:59:59.999999"
