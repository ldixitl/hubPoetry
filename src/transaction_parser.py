import logging
from typing import Dict, List

import pandas as pd

logger = logging.getLogger("parser")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/transaction_parser.log", mode="w", encoding="UTF-8")
file_formater = logging.Formatter(
    "%(asctime)s - %(filename)s - %(levelname)s: %(message)s", datefmt="%d-%m-%Y %H:%M:%S"
)
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)


def parse_transaction_auto(file_path: str) -> List[Dict]:
    """
    Принимает путь до файла формата 'CSV' или 'XLSX' и возвращает из него список словарей операций.
    При возникновении ошибки - возвращает пустой список.
    """
    try:
        logger.info(f"Вызов функции 'parse_transaction' с параметром: {file_path}")
        if file_path.endswith(".csv"):
            dataframe = pd.read_csv(file_path, sep=";")
        elif file_path.endswith(".xlsx"):
            dataframe = pd.read_excel(file_path)
        else:
            logger.error(f"Неподдерживаемый формат файла '{file_path}'", exc_info=True)
            return []

        transactions = dataframe.to_dict(orient="records")
        logger.info(f"Файл '{file_path}' успешно загружен. Найдено {len(transactions)} операций")
        return transactions

    except FileNotFoundError:
        logger.error(f"Файл по пути '{file_path}' не найден", exc_info=True)
        return []
    except pd.errors.EmptyDataError:
        logger.warning(f"Файл '{file_path}' пустой.", exc_info=True)
        return []
    except Exception as e:
        logger.error(f"Произошла ошибка при обработке файла '{file_path}': {e}", exc_info=True)
        return []
