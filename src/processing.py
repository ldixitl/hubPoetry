from typing import List, Dict


def filter_by_state(operations: List[Dict], state: str ='EXECUTED') -> List[Dict]:
    """Функция фильтрует список словарей по значению ключа 'state' и возвращает их список"""
    filtered_operations = []
    for operation in operations:
        if operation["state"] == state:
            filtered_operations.append(operation)
    return filtered_operations
