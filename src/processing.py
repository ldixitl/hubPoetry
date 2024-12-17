from typing import Dict, List


def filter_by_state(operations: List[Dict], state: str = "EXECUTED") -> List[Dict]:
    """Функция фильтрует список операций по значению ключа 'state' и возвращает отфильтрованный список"""
    filtered_operations = []
    for operation in operations:
        if operation["state"] == state:
            filtered_operations.append(operation)
    return filtered_operations


def sort_by_date(operations: List[Dict], if_reverse: bool = True) -> List[Dict]:
    """Функция сортирует списки операций по дате и возвращает отсортированный список"""
    sorted_operations = sorted(operations, key=lambda x: x["date"], reverse=if_reverse)
    return sorted_operations
