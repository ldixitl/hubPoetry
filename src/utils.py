import json
import os


def load_transactions(file_path: str) -> list:
    """Принимает путь до файла JSON и возвращает из него список словарей операций"""
    try:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="UTF-8") as json_file:
                operations = json.load(json_file)
                if isinstance(operations, list):
                    return operations
                else:
                    return []
        else:
            return []
    except Exception as e:
        print(f"Something went wrong: {e}")
        return []
