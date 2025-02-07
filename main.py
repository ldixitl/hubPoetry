import logging
import os
import time

import src.filters
import src.generators
import src.processing
import src.transaction_parser
import src.utils
import src.widget

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/main.log", mode="w", encoding="UTF-8")
file_formater = logging.Formatter(
    "%(asctime)s - %(filename)s - %(levelname)s: %(message)s", datefmt="%d-%m-%Y %H:%M:%S"
)
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)


def main() -> None:
    """Главная функция для работы приложения"""
    try:
        logger.info("Начало работы приложения.")
        print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
        time.sleep(0.5)

        # Выбор типа файла
        logger.info("Запрос у пользователя: выбор типа файла для получения информации о транзакциях.")
        print("\nВыберите необходимый пункт меню:")
        time.sleep(0.5)
        print(
            """1. Получить информацию о транзакциях из JSON-файла
2. Получить информацию о транзакциях из CSV/XLSX-файла"""
        )

        while True:
            user_choice_type = input("Ваш выбор (1-2): ").strip()
            logger.info(f"Пользователь ввёл: {user_choice_type}")

            if user_choice_type in {"1", "2"}:
                logger.info("Запрос у пользователя: путь до файла.")
                file_path = input("Введите путь до файла: ").strip()

                if not os.path.isfile(file_path):
                    logger.info(f"Некорректный ввод: {file_path}. Пользователю предложено повторить ввод.")
                    print("Некорректный путь к файлу. Повторите ввод.")
                    continue

                logger.info(f"Пользователь указал путь: {file_path}")

                if user_choice_type == "1":
                    logger.info("Пользователь выбрал JSON-файл.")
                    print("Выбран JSON-файл.")
                    transaction_list = src.utils.load_transactions(file_path)
                    logger.info(f"Загружено {len(transaction_list)} транзакций из JSON-файла.")
                else:
                    logger.info("Пользователь выбрал CSV/XLSX-файл.")
                    print("Выбран CSV/XLSX-файл.")
                    transaction_list = src.transaction_parser.parse_transaction_auto(file_path)
                    logger.info(f"Загружено {len(transaction_list)} транзакций из CSV/XLSX-файла.")
                break
            else:
                logger.info(f"Некорректный ввод: {user_choice_type}. Пользователю предложено повторить ввод.")
                print("Некорректный пункт меню. Повторите ввод.")

        # Фильтрация по статусу
        logger.info("Запрос у пользователя: выбор статуса для фильтрации.")
        valid_statuses = {"EXECUTED", "CANCELED", "PENDING"}
        print("\nВведите статус для фильтрации.")
        time.sleep(0.5)
        print(f"Доступные статусы: {', '.join(valid_statuses)}")

        while True:
            user_choice_status = input("Введите статус: ").strip().upper()
            logger.info(f"Пользователь ввёл: {user_choice_status}")

            if user_choice_status in valid_statuses:
                filtered_transactions_by_status = src.processing.filter_by_state(transaction_list, user_choice_status)
                logger.info(
                    f"""Транзакции отфильтрованы по статусу: {user_choice_status}.
Количество транзакций после фильтрации: {len(filtered_transactions_by_status)}"""
                )
                break
            else:
                logger.info(f"Некорректный статус: {user_choice_status}. Пользователю предложено повторить ввод.")
                print(f"Некорректный статус: {user_choice_status}. Повторите ввод.")

        # Сортировка по дате
        logger.info("Пользователю предложено отсортировать операции по дате.")
        print("\nОтсортировать операции по дате? Да/Нет")

        while True:
            user_choice_date_filter = input("Введите ответ: ").strip().lower()
            logger.info(f"Пользователь ввёл: {user_choice_date_filter}")

            if user_choice_date_filter == "да":
                logger.info("Пользователь выбрал сортировку операций по дате.")
                logger.info("Запрос у пользователя: выбор порядка сортировки по дате.")
                order_map = {"1": False, "2": True}
                print("\nВыберите порядок сортировки:")
                print(
                    """1. По возрастанию
2. По убыванию"""
                )

                while True:
                    user_choice_reverse = input("Введите (1-2): ").strip()
                    logger.info(f"Пользователь ввёл: {user_choice_reverse}")

                    if user_choice_reverse in order_map:
                        sorted_transactions_by_date = src.processing.sort_by_date(
                            filtered_transactions_by_status, if_reverse=order_map[user_choice_reverse]
                        )
                        logger.info(
                            f"""Транзакции отсортированы по:
{'возрастанию' if not order_map[user_choice_reverse] else 'убыванию'}."""
                        )
                        break
                    else:
                        logger.info(
                            f"Некорректный ввод: {user_choice_reverse}. Пользователю предложено повторить ввод."
                        )
                        print("Некорректный ответ. Повторите ввод.")
                break

            elif user_choice_date_filter == "нет":
                logger.info("Пользователь отказался от сортировки операций по дате.")
                sorted_transactions_by_date = filtered_transactions_by_status
                break
            else:
                logger.info(f"Некорректный ввод: {user_choice_date_filter}. Пользователю предложено повторить ввод.")
                print("Некорректный ответ. Введите 'Да' или 'Нет'.")

        # Сортировка по валюте
        logger.info("Пользователю предложено отфильтровать транзакции по типу валюты.")
        print("\nХотите отфильтровать транзакции по типу валюты?")

        available_currencies = {
            transaction.get("operationAmount", {}).get("currency", {}).get("code") or transaction.get("currency_code")
            for transaction in sorted_transactions_by_date
            if transaction.get("operationAmount", {}).get("currency") or transaction.get("currency_code")
        }

        while True:
            user_choice_currency = (
                input(f"Доступные валюты: {', '.join(available_currencies)}\nВведите код валюты или 'Нет': ")
                .strip()
                .upper()
            )
            logger.info(f"Пользователь ввёл: {user_choice_currency}")

            if user_choice_currency in available_currencies:
                logger.info(f"Пользователь выбрал фильтрацию по валюте: {user_choice_currency}")
                sorted_transactions_by_currency = list(
                    src.generators.filter_by_currency(sorted_transactions_by_date, user_choice_currency)
                )
                logger.info(
                    f"""Транзакции отфильтрованы по валюте: {user_choice_currency}.
Количество транзакций после фильтрации: {len(sorted_transactions_by_currency)}"""
                )
                break
            elif user_choice_currency == "НЕТ":
                logger.info("Пользователь отказался от фильтрации транзакций по типу валюты.")
                sorted_transactions_by_currency = sorted_transactions_by_date
                break
            else:
                logger.info(f"Некорректный ввод: {user_choice_currency}. Пользователю предложено повторить ввод.")
                print("Некорректный ответ. Введите код валюты или 'Нет'.")

        # Сортировка по описанию
        logger.info("Пользователю предложено отфильтровать транзакции по определённому слову в описании.")
        print("\nОтфильтровать список транзакций по определенному слову в описании? Да/Нет")

        while True:
            user_choice_description = input("Введите ответ: ").strip().title()
            logger.info(f"Пользователь ввёл: {user_choice_description}")

            if user_choice_description == "Да":
                logger.info("Пользователь выбрал фильтрацию транзакций по слову в описании.")
                logger.info("Запрос у пользователя: выбор слова для сортировки.")
                word_to_sort = input("Введите слово для фильтрации: ")
                logger.info(f"Пользователь ввёл: {word_to_sort}")

                sorted_transactions_by_description = src.filters.filter_transactions_by_description(
                    sorted_transactions_by_currency, word_to_sort
                )
                logger.info(
                    f"""Транзакции отфильтрованы по слову: {word_to_sort}.
Количество транзакций после фильтрации: {len(sorted_transactions_by_description)}"""
                )
                break
            elif user_choice_description == "Нет":
                logger.info("Пользователь отказался от фильтрации транзакций по слову в описании.")
                sorted_transactions_by_description = sorted_transactions_by_currency
                break
            else:
                logger.info(f"Некорректный ввод: {user_choice_description}. Пользователю предложено повторить ввод.")
                print("Некорректный ответ. Введите 'Да' или 'Нет'.")

        # Печать списка
        if len(sorted_transactions_by_description) > 0:
            logger.info("Начат вывод итогового списка транзакций.")
            print("Распечатываю итоговый список транзакций...")
            time.sleep(0.5)
            print(f"\nВсего банковских операций в выборке: {len(sorted_transactions_by_description)}")
            time.sleep(1)
            for transaction in sorted_transactions_by_description:
                date = src.widget.get_date(transaction.get("date", "Дата неизвестна"))
                description = transaction.get("description", "Без описания")
                amount = transaction.get("operationAmount", {}).get("amount") or transaction.get("amount")
                currency = transaction.get("operationAmount", {}).get("currency", {}).get("code") or transaction.get(
                    "currency_code"
                )

                sender = transaction.get("from")
                payee = transaction.get("to")

                if isinstance(sender, str) and not isinstance(sender, float):
                    sender_masked = src.widget.mask_account_card(sender)
                    payee_masked = src.widget.mask_account_card(payee)

                    print(f"\n{date} {description}\n{sender_masked} -> {payee_masked}\nСумма: {amount} {currency}")
                else:
                    payee_masked = src.widget.mask_account_card(payee)
                    print(
                        f"""\n{date} {description}
{payee_masked}
Сумма: {amount} {currency}"""
                    )
        else:
            logger.info("Не найдено транзакций, подходящих под условия.")
            print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}", exc_info=True)
    finally:
        logger.info("Завершение работы приложения")


if __name__ == "__main__":
    main()
