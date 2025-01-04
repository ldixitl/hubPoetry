from typing import Dict, Generator, List


def filter_by_currency(transaction_list: List[Dict], currency_type: str) -> Generator:
    """Функция фильтрует принимаемые транзакции по заданной валюте
    и возвращает итератор по отфильтрованным транзакциям"""
    for transaction in transaction_list:
        if transaction["operationAmount"]["currency"]["code"] == currency_type:
            yield transaction


def transaction_descriptions(transaction_list: List[Dict]) -> Generator:
    """Функция принимает список транзакций и возвращает описание каждой поочерёдно"""
    for transaction in transaction_list:
        yield transaction["description"]


def card_number_generator(start: int, stop: int) -> Generator:
    """Функция принимает начало и конец диапазона и генерирует номера банковских карт в формате XXXX XXXX XXXX XXXX"""
    for number in range(start, stop):
        card_number = str(number)
        while len(card_number) < 16:
            card_number = "0" + card_number
        final_card_number = f"{card_number[0:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:16]}"
        yield final_card_number
