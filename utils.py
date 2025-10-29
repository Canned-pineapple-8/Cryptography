import os
import cypher


def show_examples():
    """
    Вспомогательная функция для вывода примеров
    :return: None
    """
    # Пример 1
    print("\n\tПример 1. Шифрование и дешифрование")
    pt = [int(x) for x in hex_to_binary("0123456789abcdef")]
    key = [int(x) for x in hex_to_binary("133457799BBCDFF1")]
    hex_pt = binary_to_hex(''.join(map(str, pt)))
    hex_key = binary_to_hex(''.join(map(str, key)))
    ct = cypher.cypher_block(pt, key)
    hex_ct = binary_to_hex(''.join(map(str, ct)))
    dec = cypher.decypher_block(ct, key)
    hex_dec = binary_to_hex(''.join(map(str, dec)))
    print("Исходный текст:", hex_pt)
    print("Ключ:", hex_key)
    print("Шифр:", hex_ct)
    print("Расшифровка:", hex_dec)

    # Пример 2
    print("\n\tПример 2. Ошибка 1 бита")
    print("Исходный текст:", hex_pt)
    print("Шифрограмма:", hex_ct)
    ct_err = ct.copy()
    ct_err[0] ^= 1
    hex_ct_err = binary_to_hex(''.join(map(str, ct_err)))
    dec_err = cypher.decypher_block(ct_err, key)
    hex_dec_err = binary_to_hex(''.join(map(str, dec_err)))
    print("Шифрограмма с изменённым битом:", hex_ct_err)
    print("Расшифровка искажённой шифрограммы:", hex_dec_err)

    # Пример 3
    print("\n\tПример 3. Слабые ключи")
    weak_keys = ["0101010101010101", "fefefefefefefefe", "1f1f1f1f0e0e0e0e", "e0e0e0e0f1f1f1f1"]
    for wk in weak_keys:
        key = [int(x) for x in hex_to_binary(wk)]
        ct1 = cypher.cypher_block(pt, key)
        ct2 = cypher.cypher_block(ct1, key)
        print(f"\nКлюч {wk}")
        print("Исходный текст:", hex_pt)
        print("После 1 шифрования:", binary_to_hex(''.join(map(str, ct1))))
        print("После 2 шифрований:", binary_to_hex(''.join(map(str, ct2))))


def encrypt_decrypt_string():
    """
    Вспомогательная функция для шифрования/дешифрации строки в 16-чном формате
    :return: None
    """
    text = input("Введите строку (hex): ").strip()
    key_hex = input("Введите ключ (hex, 16 символов): ").strip()
    if len(key_hex) != 16 or len(text) % 16 !=0 :
        raise RuntimeError("Длина ключа должна быть равна 16, а длина строки - кратна 16.")
    pt = [int(x) for x in hex_to_binary(text)]
    key = [int(x) for x in hex_to_binary(key_hex)]
    ct = cypher.cypher_block(pt, key)
    print("Шифр:", binary_to_hex(''.join(map(str, ct))))
    dec = cypher.decypher_block(ct, key)
    print("Расшифровка:", binary_to_hex(''.join(map(str, dec))))


def encrypt_file_mode():
    """
    Вспомогательная функция для шифрования содержимого файла/записи результата в файл.
    :return: None
    """
    infile = input("Имя входного файла: ").strip()
    outfile = input("Имя файла для шифра: ").strip()
    key = input("Ключ (hex): ").strip()
    cypher.encrypt_file(infile, outfile, key)
    print("Файл зашифрован.")

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




