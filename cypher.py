import constants
from utils import assert_len, hex_to_binary, hex_to_blocks, binary_to_hex


def initial_permutation(block: list[int], ip: tuple[int] = constants.IP) -> list[int]:
    """
    Выполняет первоначальную перестановку блока
    :param block: блок длиной 64 бита (представлен списком чисел int длиной 64)
    :param ip: таблица первоначальной перестановки (представлена списком чисел int длиной 64)
    :return: блок, подвергнутый первоначальной перестановке
    """
    assert_len("Блок", block, 64)
    return [block[ip[i]] for i in range(len(ip))]


def final_permutation(block: list[int], ip_inv: tuple[int] = constants.IP_INV) -> list[int]:
    """
    Выполняет финальную перестановку блока
    :param block: блок длиной 64 бита (представлен списком чисел int длиной 64)
    :param ip_inv: таблица финальной перестановки (представлена списком чисел int длиной 64)
    :return: блок, подвергнутый финальной перестановке
    """
    assert_len("Блок", block, 64)
    return [block[ip_inv[i]] for i in range(len(ip_inv))]


def des_round(block: list[int], key: list[int]) -> list[int]:
    """
    Проведение одного из 16 этапов преобразования DES
    :param block: блок длиной 64 бита (представлен списком чисел int длиной 64)
    :param key: ключ длиной 48 бит (представлен списком чисел int длиной 48)
    :return: блок, подвергнутый очередному раунду преобразования DES
    """
    assert_len("Блок", block, 64)
    assert_len("Ключ", key, 48)

    l = block[:32]
    r = block[32:]

    r_f = f(r, key)
    new_r = [l_ ^ r_f_ for l_, r_f_ in zip(l, r_f)]  # гаммирование
    new_l = r.copy()

    return new_l + new_r


def s_blocks(gamma_block: list[int], s: tuple[tuple[tuple[int]]] = constants.S) -> list[int]:
    """
    Проход по 8 S-блокам
    :param gamma_block: подвергнутый гаммированию 48-битный блок
    :param s: кортеж из двумерных кортежей S1-8
    :return: 32-битный результирующий блок
    """
    assert_len("Блок", gamma_block, 48)

    gamma_blocks = [gamma_block[i:i + 6] for i in range(0,len(gamma_block),6)]
    result_blocks = []
    for s_i in range(len(s)):

        block = gamma_blocks[s_i]
        s_block = s[s_i]
        j = int(''.join([str(x) for x in block[1:5]]), 2)
        i = int(''.join([str(x) for x in [block[0], block[5]]]), 2)

        result_blocks.append([int(x) for x in format(s_block[i][j],'04b')])

    result_block = []
    for block in result_blocks:
        for el in block:
            result_block.append(el)

    return result_block


def p_permutation(block: list[int], p: tuple[int] = constants.P) -> list[int]:
    """
    Выполнение P-перестановки
    :param block: 32-битный исходный блок (список из int длиной 32)
    :param p: таблица P-перестановки (кортеж из int Длиной 32)
    :return: блок, подвергнутый P-перестановке
    """
    assert_len("Блок", block, 32)
    return [block[i] for i in p]


def f(r: list[int], key: list[int]) -> list[int]:
    """
    Модификация f(r[i-1], k[i])
    :param r: исходный 32-битный полублок
    :param key: 48-битный ключ
    :return: 32-битный результирующий полублок
    """
    assert_len("Блок", r, 32)
    assert_len("Ключ", key, 48)

    exp_r = expand_e(r)  # 32 -> 48 бит
    gamma_r = [el ^ k for el, k in zip(exp_r, key)]  # гаммирование
    s_bl_r = s_blocks(gamma_r)
    perm_r = p_permutation(s_bl_r)

    return perm_r


def expand_e(block: list[int], e: tuple[int] = constants.E) -> list[int]:
    """
    Расширение E
    :param block: 32-битный полублок R (представлен списком чисел int длиной 32)
    :param e: таблица расширения (представлена кортежем чисел int длиной 48)
    :return: расширенный 48-битный блок R
    """
    assert_len("Блок", block, 32)
    return [block[e[i]] for i in range(len(e))]


def cycle_shift(block: list[int], i: int, ls: tuple[int] = constants.LS) -> list[int]:
    """
    Циклический сдвиг влево
    :param i: номер раунда (0 <= i <= 15)
    :param block: блок размером 28 бит (список из 28 чисел int)
    :param ls: таблица со значениями сдвига для каждого раунда (кортеж из 16 чисел int)
    :return: Смещённый влево на ls[i] позиций блок
    """
    if i < 0 or i > 15:
        raise RuntimeError(f"Номер раунда должен быть в диапазоне 0..15 (текущее значение {i})")
    assert_len("Блок", block, 28)
    shift = ls[i]
    return block[shift:] + block[:shift]


def pc1_permutation(k: list[int], pc1: tuple[int] = constants.PC1) -> list[int]:
    """
    Выполнение перестановки PC1 из 64-битного исходного ключа
    :param k: исходный 64-битовый ключ (список int длиной 64)
    :param pc1: таблица перестановки PC1 (56 бит)
    :return: ключ длиной 56 бит, подвергнутый PC1-перестановке
    """
    assert_len("Ключ", k, 64)
    return [k[i] for i in pc1]


def pc2_permutation(k: list[int], pc2: tuple[int] = constants.PC2) -> list[int]:
    """
    Выполнение перестановки PC2 из 56-битного исходного ключа
    :param k: исходный 56-битовый ключ (список int длиной 56)
    :param pc2: таблица перестановки PC2 (56 бит)
    :return: ключ длиной 56 бит, подвергнутый PC2-перестановке
    """
    assert_len("Ключ", k, 56)
    return [k[i] for i in pc2]


def gen_keys(k: list[int], pc2: tuple[int] = constants.PC2, ls: tuple[int] = constants.LS) -> tuple[tuple[int]]:
    """
    Генерация 16 наборов 48-битовых ключей из исходного 64-битового ключа
    :param k: исходный 64-битовый ключ (кортеж int длиной 64)
    :param pc2: таблица перестановки PC2 (56 бит)
    :param ls: таблица со значениями сдвигов для каждого раунда (длина 16)
    :return: кортеж из 16 кортежей ключей длиной 48 бит каждый
    """
    assert_len("Ключ", k, 64)

    keys = []

    key_pc1 = pc1_permutation(k)
    l, r = key_pc1[:28], key_pc1[28:]

    for des_round_i in range(16):
        l = cycle_shift(l, des_round_i, ls)
        r = cycle_shift(r, des_round_i, ls)

        key_shifted = l + r
        keys.append(tuple(pc2_permutation(key_shifted)))

    return tuple(keys)


def cypher_block(block: list[int], key:list[int]) -> list[int]:
    """
    Зашифровать один блок
    :param block: 64-битный блок открытого текста
    :param key: 64-битный исходный ключ
    :return: зашифрованный 64-битный текст
    """
    assert_len("Блок", block, 64)
    assert_len("Ключ", key, 64)

    keys = gen_keys(key)

    p1_block = initial_permutation(block)
    for round_i in range(16):
        p1_block = des_round(p1_block, keys[round_i])

    p2_block = p1_block[32:] + p1_block[:32]

    p2_block = final_permutation(p2_block)

    return p2_block


def decypher_block(block: list[int], key:list[int]) -> list[int]:
    """
    Расшифровать один блок
    :param block: 64-битный блок шифрограммы
    :param key: 64-битный исходный ключ
    :return: расшифрованный 64-битный текст
    """

    assert_len("Блок", block, 64)
    assert_len("Ключ", key, 64)

    keys = gen_keys(key)

    p1_block = initial_permutation(block)
    # применяем ту же функцию des_round, но ключи в обратном порядке
    for round_i in range(15, -1, -1):
        p1_block = des_round(p1_block, keys[round_i])

    p2_block = p1_block[32:] + p1_block[:32]
    p2_block = final_permutation(p2_block)

    return p2_block


def encrypt_file(in_filename: str, out_filename: str, key: str):
    """
    Осуществляет шифрование открытого текста, указанного в файле
    :param in_filename: путь к файлу, текст которого требуется зашифровать
    :param out_filename: путь к файлу, в который требуется записать зашифрованный текст
    :param key: ключ в формате 16-чной строки
    :return: void
    """
    key = [int(x) for x in hex_to_binary(key)]
    assert_len("Ключ", key, 64)

    # Чтение файла в бинарном режиме
    with open(in_filename, "rb") as f:
        plaintext_bytes = f.read()

    # Преобразование байтов в hex-строку
    hex_text = plaintext_bytes.hex()

    text_blocks = hex_to_blocks(hex_text)
    result_hex = ""
    for block in text_blocks:
        crypted_block = cypher_block(block, key)
        result_hex += binary_to_hex(''.join([str(x) for x in crypted_block]))

    # Запись зашифрованных данных в бинарном режиме
    result_bytes = bytes.fromhex(result_hex)
    with open(out_filename, "wb") as f:
        f.write(result_bytes)
