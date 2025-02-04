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
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)
    return [transaction for transaction in transaction_list if pattern.search(transaction.get("description", ""))]


def count_transactions_by_category(transaction_list: List[Dict], category_list: List) -> Dict:
    """
    Подсчитывает количество транзакций в каждой категории.

    :param transaction_list: Список словарей с данными о транзакциях
    :param category_list: Список категорий транзакций
    :return: Словарь, в котором ключи — это названия категорий, а значения — это количество операций в каждой категории
    """
    # Убираем возможные повторения категорий
    category_list = list(set(category.lower() for category in category_list))
    category_count = Counter()
    for category in category_list:
        pattern = re.compile(re.escape(category), re.IGNORECASE)

        for transaction in transaction_list:
            if pattern.search(transaction.get("description", "")):
                category_count[category] += 1

    return dict(category_count)
