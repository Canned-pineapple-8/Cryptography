import os
import cypher


def show_examples(c0: str):
    """
    Вспомогательная функция для вывода примеров
    :param: c0 - начальный вектор C0
    :return: None
    """
    # Пример 1
    print("\n\tПример 1. Шифрование и дешифрование")
    pt = "0123456789abcdef0123456789abcdef"
    key = "133457799BBCDFF1"

    ct = cypher.encrypt_text(pt, key, c0)
    dt = cypher.decrypt_text(ct, key, c0)

    print("Исходный текст:", pt)
    print("Ключ:", key)
    print("Вектор C:", c0)
    print("Шифр:", ct)
    print("Расшифровка:", dt)

    # Пример 2
    print("\n\tПример 2. Ошибка 1 бита")
    print("Исходный текст:", pt)
    print("Шифрограмма:", ct)
    ct_err = [int(x) for x in hex_to_binary(ct)]
    ct_err[0] ^= 1
    ct_err_hex = binary_to_hex(''.join([str(x) for x in ct_err]))
    dt_err_hex = cypher.decrypt_text(ct_err_hex, key, c0)
    print("Шифрограмма с изменённым битом:", ct_err_hex)
    print("Расшифровка искажённой шифрограммы:", dt_err_hex)

    # Пример 3
    print("\n\tПример 3. Слабые ключи")
    weak_keys = ["0101010101010101", "fefefefefefefefe", "1f1f1f1f0e0e0e0e", "e0e0e0e0f1f1f1f1"]
    for wk in weak_keys:
        ct1 = cypher.encrypt_text(pt, wk, c0)
        ct2 = cypher.encrypt_text(ct1, wk, c0)
        print(f"\nКлюч {wk}")
        print("Исходный текст:", pt)
        print("После 1 шифрования:", ct1)
        print("После 2 шифрований:", ct2)


def encrypt_string(c0: str):
    """
    Вспомогательная функция для шифрования строки в 16-чном формате
    :return: None
    """
    text = input("Введите строку (hex): ").strip()
    key_hex = input("Введите ключ (hex, 16 символов): ").strip()

    if len(key_hex) != 16 or len(c0) != 16:
        raise RuntimeError("Длина ключа и вектора C должна быть равна 16.")

    print(f"Вектор С0: {c0}")
    crypted_text = cypher.encrypt_text(text, key_hex, c0)

    print("Шифр:", crypted_text)


def decrypt_string(c0: str):
    """
    Вспомогательная функция для дешифрования строки в 16-чном формате
    :return: None
    """
    text = input("Введите строку (hex): ").strip()
    key_hex = input("Введите ключ (hex, 16 символов): ").strip()

    if len(key_hex) != 16 or len(c0) != 16:
        raise RuntimeError("Длина ключа и вектора C должна быть равна 16.")

    print(f"Вектор С0: {c0}")
    decrypted_text = cypher.decrypt_text(text, key_hex, c0)
    print("Расшифровка:", decrypted_text)


def encrypt_file_mode(c0: str):
    """
    Вспомогательная функция для шифрования содержимого файла/записи результата в файл.
    :return: None
    """
    infile = input("Имя входного файла с исходным текстом: ").strip()
    outfile = input("Имя файла для помещения шифра: ").strip()
    key = input("Ключ (hex): ").strip()
    print(f"Вектор С0: {c0}")
    result = cypher.encrypt_file(infile, outfile, key, c0)
    if result == 0:
        print("Файл зашифрован.")


def decrypt_file_mode(c0: str):
    """
    Вспомогательная функция для дешифрования содержимого файла/записи результата в файл.
    :return: None
    """
    infile = input("Имя входного файла с шифром: ").strip()
    outfile = input("Имя файла для помещения расшифровки: ").strip()
    key = input("Ключ (hex): ").strip()
    print(f"Вектор С0: {c0}")
    result = cypher.decrypt_file(infile, outfile, key, c0)
    if result == 0:
        print("Файл расшифрован.")


def binary_to_hex(bin_str:str) -> str:
    """
    Конвертация строки в бинарном формате в строку в 16-чной СС
    :param bin_str: строка в бинарном формате
    :return: строка в 16-чной СС
    """
    if len(bin_str) % 4 != 0:
        bin_str = bin_str + "0" * (4 - len(bin_str) % 4)
    return ''.join([format(int(bin_str[i:i + 4], 2), 'x')
                          for i in range(0, len(bin_str), 4)])


def hex_to_binary(hex_str: str) -> str:
    """
    Конвертация строки в 16-чной СС в бинарный формат
    :param hex_str: строка в 16-чном формате
    :return: бинарная строка
    """
    hex_str = hex_str.lower()
    for char in hex_str:
        if char not in "0123456789abcdef":
            raise RuntimeError("Передана строка не в 16-чном формате.")
    return ''.join(bin(int(c, 16))[2:].zfill(4) for c in hex_str)


def assert_len(name: str, arr: list[int], expected: int):
    """
    Проверить соответствие длин
    :param name: параметр для информативного вывода
    :param arr: список для проверки длины
    :param expected: ожидаемая длина
    :return: None, выбрасывает RuntimeError в случае несовпадения
    """
    if len(arr) != expected:
        raise RuntimeError(f"{name} должен быть длины {expected}, но длина — {len(arr)}")


def hex_to_blocks(hex_str:str) -> list[list[int]]:
    """
    Преобразовывает 16-чную строку в массив блоков по 64 бита в бинарном представлении
    :param hex_str: строка в 16-чном формате
    :return: массив из блоков по 64 элемента, каждый из которых представлен набором нулей и единиц
    """
    str_blocks = [hex_str[i:i+16] for i in range(0, len(hex_str),16)]
    blocks = [[int(x) for x in hex_to_binary(i)] for i in str_blocks]
    return blocks


def add_padding(text_hex: str, hex_block_size:int = 16) -> str:
    """
    Добавляет символы в строку так, чтобы её длина была кратна hex_block_size (в формате hex)
    :param hex_block_size: размер блока (в 16-чном формате)
    :param text_hex: строка для модификации
    :return: модифицированная строка, длина которой кратна hex_block_size (в формате hex)
    """
    if len(text_hex) % hex_block_size == 0:
        return text_hex

    padding_length = hex_block_size - len(text_hex) % hex_block_size
    padding_char = format(padding_length, '02x')[-1]
    return text_hex + padding_char * padding_length


def remove_padding(text_hex:str) -> str:
    if len(text_hex) == 0:
        return text_hex

    padding_length = int(text_hex[-1], 16)
    if padding_length <= 0 or padding_length > 16:
        raise RuntimeError(f"Некорректное значение паддинга ({padding_length})")

    padding_part = text_hex[-padding_length:]
    if not all(c == text_hex[-1] for c in padding_part):
        return text_hex

    return text_hex[:-padding_length]
