import re
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
