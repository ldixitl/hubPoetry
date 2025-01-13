import os
import time
from functools import wraps
from typing import Any, Callable, Optional


def logger(filename: Optional[str] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Декоратор, который регистрирует выполнение функции, включая время ее начала,
    окончания, входные аргументы, результат и любые ошибки."""

    def decorator(function: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Путь для файла логов
            path = os.path.join(os.path.dirname(__file__), "..", "data", filename) if filename else None
            start_func = time.ctime(time.time())
            time.sleep(1)
            result = None
            try:
                result = function(*args, **kwargs)
                finish_func = time.ctime(time.time())

                log_message = f"""Function start: {start_func}
Function '{function.__name__}' called with args: {args} and kwargs: {kwargs}.
Result: {result}
Function finish: {finish_func}
"""
            except Exception as ex:
                log_message = f"""Function start: {start_func}
The function '{function.__name__}' failed with an error '{type(ex).__name__}: {ex}'
Inputs - args: {args} and kwargs: {kwargs}
"""
                if filename:
                    with open(str(path), "a") as log_file:
                        log_file.write(log_message)
                        log_file.write("\n")
                else:
                    print(log_message)
                raise  # Повторно выбрасываем исключение для обработки за пределами декоратора

            else:
                if filename:
                    with open(str(path), "a") as log_file:
                        log_file.write(log_message)
                        log_file.write("\n")
                else:
                    print(log_message)
            return result

        return wrapper

    return decorator
