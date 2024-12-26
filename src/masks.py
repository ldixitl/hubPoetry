def get_mask_card_number(card_number: int) -> str:
    """Функция принимает на вход номер карты и возвращает ее маску"""
    if isinstance(card_number, int):
        card_number_str = str(card_number)

        if len(card_number_str) != 16:
            raise ValueError("Номер карты должен содержать 16 цифр.")

        return f"{card_number_str[:4]} {card_number_str[4:6]}** **** {card_number_str[12:]}"
    else:
        raise TypeError("Некорректный тип данных.")


def get_mask_account(account_number: int) -> str:
    """Функция принимает номер счёта и возвращает его маску"""
    if isinstance(account_number, int):
        account_number_str = str(account_number)

        if len(account_number_str) != 20:
            raise ValueError("Номер счёта должен содержать 20 цифр.")

        return f"**{account_number_str[-4:]}"
    else:
        raise TypeError("Некорректный тип данных.")
