from unittest.mock import mock_open, patch

from src.utils import load_transactions


@patch("builtins.open", new_callable=mock_open, read_data='[{"id": 1, "amount": "100"}]')
def test_load_transactions_success(mock_file) -> None:
    """Тест успешной загрузки данных из файла"""
    file_path = "../data/operations.json"
    result = load_transactions(file_path)
    expected = [{"id": 1, "amount": "100"}]
    assert result == expected
    mock_file.assert_called_once_with(file_path, "r", encoding="UTF-8")


@patch("builtins.open", side_effect=FileNotFoundError)
def test_file_not_found(mock_file) -> None:
    """Тест случая, когда файл не найден"""
    file_path = "data/nonexistent.json"
    result = load_transactions(file_path)
    assert result == []
    mock_file.assert_called_once_with(file_path, "r", encoding="UTF-8")


@patch("builtins.open", new_callable=mock_open, read_data="[]")
def test_empty_file(mock_file) -> None:
    """Тест для пустого файла"""
    file_path = "../data/empty.json"
    result = load_transactions(file_path)
    assert result == []
    mock_file.assert_called_once_with(file_path, "r", encoding="UTF-8")


@patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
def test_file_contains_not_a_list(mock_file) -> None:
    """Тест случая, когда файл содержит не список"""
    file_path = "../data/invalid.json"
    result = load_transactions(file_path)
    assert result == []
    mock_file.assert_called_once_with(file_path, "r", encoding="UTF-8")
