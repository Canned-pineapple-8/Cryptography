import cypher
import utils, random_generator

if __name__ == "__main__":
    """
    print("1 - Примеры\n2 - Шифрование/дешифрование строки\n3 - Шифрование файла")
    choice = input("Выберите опцию: ").strip()
    try:
        if choice == "1":
            utils.show_examples()
        elif choice == "2":
            utils.encrypt_decrypt_string()
        elif choice == "3":
            utils.encrypt_file_mode()
        else:
            print("Неверный выбор.")
    except RuntimeError as e:
        print(f"Ошибка: {e}")
    """

    pngen_const = {"A": 13,
                   "B": 256,
                   "C": 43,
                   "T": 37
                   }

    c0 = random_generator.gen_c0(pngen_const)
    print(c0)
    print(len(c0))

