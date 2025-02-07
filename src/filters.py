import re
from collections import Counter
from typing import Dict, List


def filter_transactions_by_description(transaction_list: List[Dict], search_string: str) -> List[Dict]:
    """
    Фильтрует список банковских операций по строке поиска в описании.

    :param transaction_list: Список словарей с данными о транзакциях
    :param search_string: Строка поиска
    :return: Список словарей, в описании которых есть search_string
    """
    if not isinstance(transaction_list, list):
        raise TypeError("Некорректный тип данных для списка транзакций. Ожидается список словарей.")

    if not isinstance(search_string, str):
        raise TypeError("Некорректный тип данных для поиска. Ожидается строка.")

    pattern = re.compile(re.escape(search_string), re.IGNORECASE)

    filtered_transactions = []
    for transaction in transaction_list:
        description = transaction.get("description")

        if not isinstance(description, str):
            raise TypeError(f"Некорректный тип данных в описании (id={transaction.get('id')}). Ожидается строка.")

        if pattern.search(description):
            filtered_transactions.append(transaction)

    return filtered_transactions


def count_transactions_by_category(transaction_list: List[Dict], category_list: List) -> Dict:
    """
    Подсчитывает количество транзакций в каждой категории.

    :param transaction_list: Список словарей с данными о транзакциях
    :param category_list: Список категорий транзакций
    :return: Словарь, в котором ключи — это названия категорий, а значения — это количество операций в каждой категории
    """
    if not isinstance(transaction_list, list):
        raise TypeError("Некорректный тип данных для списка транзакций. Ожидается список словарей.")
    if not isinstance(category_list, list):
        raise TypeError("Некорректный тип данных для списка категорий. Ожидается список строк.")

    # Убираем возможные повторения категорий
    category_list = list(set(category.lower() for category in category_list))
    category_count = Counter()
    for category in category_list:
        pattern = re.compile(re.escape(category), re.IGNORECASE)

        for transaction in transaction_list:
            description = transaction.get("description")

            if not isinstance(description, str):
                raise TypeError(f"Некорректный тип данных в описании (id={transaction.get('id')}). Ожидается строка.")

            if pattern.search(description):
                category_count[category] += 1

    return dict(category_count)
