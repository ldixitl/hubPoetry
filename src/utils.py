import json


def load_transactions(file_path: str) -> list:
    """Принимает путь до файла JSON и возвращает из него список словарей операций"""
    try:
        with open(file_path, "r", encoding="UTF-8") as json_file:
            data = json.load(json_file)
            return data if isinstance(data, list) else []
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []
