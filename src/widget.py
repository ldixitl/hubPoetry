import logging

from dateutil import parser

from src import masks

# Настройка логирования
logger = logging.getLogger("widget")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/widget.log", mode="w", encoding="UTF-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(filename)s - %(levelname)s: %(message)s", datefmt="%d-%m-%Y %H:%M:%S"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def mask_account_card(number: str) -> str:
    """Функция принимает на вход номер карты/счёта и возвращает маску"""
    logger.info(f"Вызов функции 'mask_account_card' с параметром: {number}")

    if not isinstance(number, str):
        logger.error(f"Передан некорректный тип данных: {type(number)}")
        raise TypeError("Некорректный тип данных. Ожидается строка.")

    if number.startswith("Счет"):
        account_number = number[5:].replace(" ", "")
        if not account_number.isdigit():
            logger.error(f"Некорректный формат номера счёта: {account_number}")
            raise ValueError("Номер счёта должен содержать только цифры.")

        try:
            masked_account = masks.get_mask_account(account_number)
            logger.info(f"Номер счёта успешно замаскирован: {masked_account}")
            return f"Счет {masked_account}"
        except ValueError as e:
            logger.error(f"Ошибка при обработке номера счёта: {e}")
            raise

    if len(number) < 16:
        logger.error(f"Некорректная длина или формат номера карты: {number}")
        raise ValueError("Номер карты должен содержать минимум 16 цифр.")

    card_number = number[-16:]  # Берём последние 16 символов
    try:
        masked_card = masks.get_mask_card_number(card_number)
        logger.info(f"Номер карты успешно замаскирован: {masked_card}")
        return f"{number[:-17]} {masked_card}"
    except ValueError as e:
        logger.error(f"Ошибка при обработке номера карты: {e}")
        raise


def get_date(date: str) -> str:
    """Функция получает дату и время в ISO-8601 формате и возвращает дату"""
    if not isinstance(date, str):
        raise TypeError("Ожидается строка.")

    try:
        dt = parser.isoparse(date)
        return dt.strftime("%d.%m.%Y")
    except ValueError as e:
        raise ValueError(f"Некорректный формат даты: {e}")
