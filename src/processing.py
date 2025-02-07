from typing import Dict, List

from dateutil import parser


def filter_by_state(operations: List[Dict], state: str = "EXECUTED") -> List[Dict]:
    """Функция фильтрует список операций по значению ключа 'state' и возвращает отфильтрованный список"""
    filtered_operations = []
    for operation in operations:
        if operation.get("state") == state:
            filtered_operations.append(operation)
    return filtered_operations


def sort_by_date(operations: List[Dict], if_reverse: bool = True) -> List[Dict]:
    """Функция сортирует списки операций по дате и возвращает отсортированный список"""
    try:
        operations_with_date = [op for op in operations if "date" in op]
        operations_without_date = [op for op in operations if "date" not in op]

        sorted_operations = sorted(operations_with_date, key=lambda x: parser.isoparse(x["date"]), reverse=if_reverse)
        return sorted_operations + operations_without_date
    except ValueError as e:
        raise ValueError(f"Некорректный формат даты: {e}.")
