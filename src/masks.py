import logging

logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("../logs/masks.log", mode="w", encoding="UTF-8")
file_formater = logging.Formatter(
    "%(asctime)s - %(filename)s - %(levelname)s: %(message)s", datefmt="%d-%m-%Y %H:%M:%S"
)
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: int) -> str:
    """Функция принимает на вход номер карты и возвращает ее маску"""
    logger.info(f"Вызов функции 'get_mask_card_number' с параметром: {card_number}")
    if isinstance(card_number, int):
        card_number_str = str(card_number)

        if len(card_number_str) != 16:
            logger.error(f"Неверная длина номера карты: {len(card_number_str)}")
            raise ValueError("Номер карты должен содержать 16 цифр.")

        masked_card_number = f"{card_number_str[:4]} {card_number_str[4:6]}** **** {card_number_str[12:]}"
        logger.info(f"Номер карты успешно замаскирован: {masked_card_number}")

        return masked_card_number
    else:
        logger.error(f"Передан некорректный тип данных: {type(card_number)}")
        raise TypeError("Некорректный тип данных.")


def get_mask_account(account_number: int) -> str:
    """Функция принимает номер счёта и возвращает его маску"""
    logger.info(f"Вызов функции 'get_mask_account' с параметром: {account_number}")
    if isinstance(account_number, int):
        account_number_str = str(account_number)

        if len(account_number_str) != 20:
            logger.error(f"Неверная длина номера счёта: {len(account_number_str)}")
            raise ValueError("Номер счёта должен содержать 20 цифр.")

        masked_account_number = f"**{account_number_str[-4:]}"
        logger.info(f"Номер счёта успешно замаскирован: {masked_account_number}")

        return masked_account_number
    else:
        logger.error(f"Передан некорректный тип данных: {type(account_number)}")
        raise TypeError("Некорректный тип данных.")
