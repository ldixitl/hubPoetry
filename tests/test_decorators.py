from typing import Union

import pytest

from src.decorators import logger


@logger()
def success_function(x: int, y: int) -> int:
    return x + y


@logger()
def error_function(x: int, y: int) -> float:
    return x / y  # Ошибка, если y == 0


@logger(filename="test_log.txt")
def logged_function(x: int, y: int) -> Union[int, float]:
    return x * y


def test_success_function(capsys) -> None:
    """Проверка успешного выполнения функции и вывода в консоль."""
    result = success_function(2, 3)
    captured = capsys.readouterr()  # Перехват вывода в консоль

    assert result == 5
    assert "Function start:" in captured.out
    assert "Function 'success_function' called with args: (2, 3) and kwargs: {}." in captured.out
    assert "Result: 5" in captured.out
    assert "Function finish:" in captured.out


def test_error_function(capsys) -> None:
    """Проверка обработки исключения и вывода ошибки в консоль."""
    result = None
    with pytest.raises(ZeroDivisionError):
        result = error_function(10, 0)

    captured = capsys.readouterr()  # Перехват вывода в консоль
    assert result is None
    assert "Function start:" in captured.out
    assert "The function 'error_function' failed with an error 'ZeroDivisionError:" in captured.out
    assert "Inputs - args: (10, 0) and kwargs: {}" in captured.out


def test_logged_function_file(tmp_path) -> None:
    """Проверка записи логов в файл."""
    # Путь для временного файла
    log_file = tmp_path / "test_log.txt"

    # Создаем функцию с логированием в файл
    @logger(filename=str(log_file))
    def multiply_function(x: int, y: int) -> Union[int, float]:
        return x * y

    # Вызов функции
    result = multiply_function(4, 5)
    assert result == 20

    # Проверяем содержимое файла
    with open(log_file, "r") as file:
        content = file.read()

    assert "Function start:" in content
    assert "Function 'multiply_function' called with args: (4, 5) and kwargs: {}." in content
    assert "Result: 20" in content
    assert "Function finish:" in content


def test_logged_function_file_error(tmp_path) -> None:
    """Проверка записи ошибки в файл."""
    log_file = tmp_path / "test_error_log.txt"

    # Создаем функцию с логированием в файл
    @logger(filename=str(log_file))
    def divide_function(x: int, y: int) -> float:
        return x / y

    # Вызов функции, вызывающей ошибку
    with pytest.raises(ZeroDivisionError):
        divide_function(10, 0)

    # Проверяем содержимое файла
    with open(log_file, "r") as file:
        content = file.read()

    assert "Function start:" in content
    assert "The function 'divide_function' failed with an error 'ZeroDivisionError:" in content
    assert "Inputs - args: (10, 0) and kwargs: {}" in content
