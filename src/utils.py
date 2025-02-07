import json
import logging

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/utils.log", mode="w", encoding="UTF-8")
file_formater = logging.Formatter(
    "%(asctime)s - %(filename)s - %(levelname)s: %(message)s", datefmt="%d-%m-%Y %H:%M:%S"
)
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)


def load_transactions(file_path: str) -> list:
    """Принимает путь до файла JSON и возвращает из него список словарей операций"""
    try:
        logger.info(f"Вызов функции 'load_transaction' с параметром: {file_path}")
        with open(file_path, "r", encoding="UTF-8") as json_file:
            data = json.load(json_file)
            if isinstance(data, list):
                logger.info(f"Файл '{file_path}' успешно загружен. Найдено {len(data)} операций")
                return data
            else:
                logger.warning(f"Данные в файле '{file_path}' не являются списком. Возвращён пустой список.")
                return []
    except FileNotFoundError:
        logger.error(f"Файл по пути '{file_path}' не найден", exc_info=True)
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON файла '{file_path}': {e}", exc_info=True)
        return []
    except Exception as e:
        logger.error(f"Произошла ошибка при обработке файла '{file_path}': {e}", exc_info=True)
        return []
