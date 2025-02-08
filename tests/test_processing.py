from typing import Dict, List

import pytest

from src.processing import filter_by_state, sort_by_date


def test_filter_by_state_executed(operations_list: List[Dict]) -> None:
    assert filter_by_state(operations_list) == [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]


def test_filter_by_state_canceled(operations_list: List[Dict]) -> None:
    assert filter_by_state(operations_list, "CANCELED") == [
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


def test_filter_by_state_empty(operations_list: List[Dict]) -> None:
    assert filter_by_state(operations_list, "OPENED") == []


@pytest.mark.parametrize(
    "if_reverse, expected",
    [
        (
            True,
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
        ),
        (
            False,
            [
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            ],
        ),
    ],
)
def test_sort_by_date(operations_list: List[Dict], if_reverse: bool, expected: List[Dict]) -> None:
    assert sort_by_date(operations_list, if_reverse) == expected


def test_sort_by_date_same_dates() -> None:
    assert sort_by_date(
        [
            {"id": 1, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            {"id": 2, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        ]
    ) == [
        {"id": 1, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 2, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    ]


def test_sort_by_date_invalid_format() -> None:
    with pytest.raises(ValueError):
        sort_by_date(
            [
                {"id": 1, "state": "EXECUTED", "date": "invalid_date"},
                {"id": 2, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            ]
        )
