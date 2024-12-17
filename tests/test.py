import os
from typing import List

import langdetect


def get_names_from_file(file_name: str) -> List[str]:
    """Функция принимает имя файла и возвращает список имен, содержащихся в файле"""
    curr_dir = os.path.dirname(__file__)

    path_to_file = os.path.join(curr_dir, "..", "data", file_name)
    path_to_file = os.path.normpath(path_to_file)

    cleaned_names = []

    with open(path_to_file, "r", encoding="utf-8") as file:
        file_content = file.read()

    for char in file_content:
        if char.isalpha() or char.isspace():
            cleaned_names.append(char)

    cleaned_names_str = "".join(cleaned_names)

    names_list = []
    for name in cleaned_names_str.split():
        name = name.strip()
        names_list.append(name)

    return names_list


def get_russian_name(my_list: List[str]) -> None:
    russian_names = []
    for name in my_list:
        if langdetect.detect(name) == "ru":
            russian_names.append(name)

    russian_names = sorted(russian_names)

    with open("../data/russian_names.txt", "w", encoding="utf-8") as file:
        for name in russian_names:
            file.write(name)
            file.write("\n")

    return print("Файл создан в папке 'data/'")


def get_english_name(my_list: List[str]) -> None:
    english_names = []
    for name in my_list:
        if langdetect.detect(name) == "en":
            english_names.append(name)

    english_names = sorted(english_names)

    with open("../data/english_names.txt", "w", encoding="utf-8") as file:
        for name in english_names:
            file.write(name)
            file.write("\n")

    return print("Файл создан в папке 'data/'")


names = get_names_from_file("names.txt")
get_english_name(names)
