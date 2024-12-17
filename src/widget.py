import masks


def mask_account_card(number: str) -> str:
    """Функция принимает на вход номер карты/счёта и возвращает маску"""
    if number.startswith("Счет"):
        return f"Счет {masks.get_mask_account(int(number[-5:]))}"
    else:
        card_number = number[-17:]
        return f"{number[:-17]} {masks.get_mask_card_number(int(card_number))}"


def get_date(date: str) -> str:
    """Функция получает дату и время в формате '2024-03-11T02:26:18.671407' и возвращает дату"""
    return f"{date[8:10]}.{date[5:7]}.{date[:4]}"
