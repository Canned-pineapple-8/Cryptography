import cypher
import utils, random_generator

if __name__ == "__main__":

    pngen_const = {"A": 13,
                   "B": 256,
                   "C": 43,
                   "T": 37
                   }

    c0 = random_generator.gen_c0(pngen_const)
    hex_c0 = utils.binary_to_hex(''.join([str(x) for x in c0]))

    print("1 - Примеры\n2 - Шифрование строки\n3 - Дешифрование строки\n4 - Шифрование файла\n5 - Дешифрование файла")
    choice = input("Выберите опцию: ").strip()
    k = int(input("Введите размер блока k: "))
    if k < 1 or k > 64 or k % 4 != 0:
        print("Введено неверное значение блока k (условия корректного k: 1 <= k <= 64 и k кратно 4).")
        exit()
    try:
        if choice == "1":
            utils.show_examples(hex_c0, k)
        elif choice == "2":
            utils.encrypt_string(hex_c0, k)
        elif choice == "3":
            utils.decrypt_string(hex_c0, k)
        elif choice == "4":
            utils.encrypt_file_mode(hex_c0, k)
        elif choice == "5":
            utils.decrypt_file_mode(hex_c0, k)
        else:
            print("Неверный выбор.")
    except RuntimeError as e:
        print(f"Ошибка: {e}")

