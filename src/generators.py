from typing import Dict, Generator, List


def filter_by_currency(transaction_list: List[Dict], currency_type: str) -> Generator:
    """Функция фильтрует принимаемые транзакции по заданной валюте
    и возвращает итератор по отфильтрованным транзакциям"""
    if isinstance(transaction_list, list):
        for transaction in transaction_list:
            if (
                transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency_type.upper()
                or transaction.get("currency_code") == currency_type.upper()
            ):
                yield transaction
    else:
        raise TypeError("Некорректный тип данных.")


def transaction_descriptions(transaction_list: List[Dict]) -> Generator:
    """Функция принимает список транзакций и возвращает описание каждой поочерёдно"""
    if isinstance(transaction_list, list):
        for transaction in transaction_list:
            if "description" in transaction:
                yield transaction["description"]
            else:
                raise KeyError(f"Отсутствует ключ 'description' в элементе: {transaction}")
    else:
        raise TypeError("Некорректный тип данных.")


def card_number_generator(start: int, stop: int) -> Generator:
    """Функция принимает начало и конец диапазона и генерирует номера банковских карт в формате XXXX XXXX XXXX XXXX"""
    if isinstance(start, int) and isinstance(stop, int):
        if start <= stop:
            for number in range(start, stop + 1):
                card_number = str(number)
                while len(card_number) < 16:
                    card_number = "0" + card_number
                final_card_number = f"{card_number[0:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:16]}"
                yield final_card_number
        else:
            raise ValueError("Некорректно заданны значения.")
    else:
        raise TypeError("Некорректный тип данных.")
