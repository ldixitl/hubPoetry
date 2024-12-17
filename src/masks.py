def get_mask_card_number(card_number: int) -> str:
    """Функция принимает на вход номер карты и возвращает ее маску"""
    card_number_str = str(card_number)

    if len(card_number_str) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр.")

    return f"{card_number_str[:4]} {card_number_str[4:6]}** **** {card_number_str[12:]}"


def get_mask_account(account_number: int) -> str:
    """Функция принимает номер счёта и возвращает его маску"""
    account_number_str = str(account_number)
    return f"**{account_number_str[-4:]}"
