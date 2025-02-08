import logging

# Настройка логирования
logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/masks.log", mode="w", encoding="UTF-8")
file_formater = logging.Formatter(
    "%(asctime)s - %(filename)s - %(levelname)s: %(message)s", datefmt="%d-%m-%Y %H:%M:%S"
)
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Функция принимает на вход номер карты (строка) и возвращает её маску"""
    logger.info(f"Вызов функции 'get_mask_card_number' с параметром: {card_number}")

    if not isinstance(card_number, str):
        logger.error(f"Передан некорректный тип данных: {type(card_number)}")
        raise TypeError("Некорректный тип данных. Ожидается строка.")

    if len(card_number) != 16 or not card_number.isdigit():
        logger.error(f"Неверная длина или формат номера карты: {card_number}")
        raise ValueError("Номер карты должен содержать 16 цифр.")

    masked_card_number = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[12:]}"
    logger.info(f"Номер карты успешно замаскирован: {masked_card_number}")

    return masked_card_number


def get_mask_account(account_number: str) -> str:
    """Функция принимает номер счёта (строка) и возвращает его маску"""
    logger.info(f"Вызов функции 'get_mask_account' с параметром: {account_number}")

    if not isinstance(account_number, str):
        logger.error(f"Передан некорректный тип данных: {type(account_number)}")
        raise TypeError("Некорректный тип данных. Ожидается строка.")

    if len(account_number) != 20 or not account_number.isdigit():
        logger.error(f"Неверная длина или формат номера счёта: {account_number}")
        raise ValueError("Номер счёта должен содержать 20 цифр.")

    masked_account_number = f"**{account_number[-4:]}"
    logger.info(f"Номер счёта успешно замаскирован: {masked_account_number}")

    return masked_account_number
