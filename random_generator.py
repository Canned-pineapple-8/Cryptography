from typing import *
from math import log2
from constants import c0_length

def pn_gen(seq: List[int], ind: int, constants: Dict[str,int]) -> int:
    """
    Генератор псевдослучайных чисел (ПСЧ)
    T(i+1) = (A * T(i) + C) mod B
    :param seq: структура, которая заполняется псевдослучайными числами (T(i))
    :param ind: индекс псевдослучайного числа, которое нужно получить (T(ind))
    :param constants: константы для вычисления (A,B,C,T0). Словарь вида {"A": <число>, "B": <число>, "C": <число>, "T": <число> }
    :return: T(ind)
    """
    if ind == 0:
        if len(seq) == 0:
            seq.append(constants["T"])
        return seq[0]

    if ind < len(seq):
        return seq[ind]
    if len(seq) == 0:
        seq.append(constants["T"])
    for i in range(len(seq), ind + 1):
        seq.append((constants["A"] * seq[i - 1] + constants["C"]) % constants["B"])

    return seq[ind]


def gen_c0(constants: Dict[str, int]) -> List[int]:
    """

    :param constants:
    :return:
    """
    b = constants["B"]
    if b < 1:
        raise RuntimeError(f"Значение B должно быть больше 0 (текущее значение {b})")
    if b == 2 ** (int(log2(b))):
        word_length = int(log2(b))
    else:
        word_length = int(log2(b)) + 1

    if c0_length % word_length == 0:
        word_amt = c0_length // word_length
    else:
        word_amt = c0_length // word_length + 1

    words = []
    pn_gen(words, word_amt - 1, constants)

    binary_word = ''.join([bin(x)[2:].zfill(word_length) for x in words])[:c0_length]
    return [int(x) for x in binary_word]