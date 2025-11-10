import os
import random
import string
import numpy as np


def generate_random_name(length):
    """Генерує випадкову назву фіксованої довжини."""
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def generate_random_content(min_len, max_len):
    """Генерує випадковий текстовий вміст у заданому діапазоні."""
    length = random.randint(min_len, max_len)
    chars = string.ascii_letters + string.digits + ' \n'
    return ''.join(random.choice(chars) for _ in range(length))


def generate_numpy_content(min_len: int, max_len: int) -> str:
    NUMPY_CHAR_RANGE = 9
    """
    Генерує випадковий вміст (послідовність чисел) у заданому діапазоні
    символів, використовуючи NumPy для прискорення генерації.
    """
    length = random.randint(min_len, max_len)

    data = np.random.randint(
        0,
        NUMPY_CHAR_RANGE,
        size=length,
        dtype=np.uint8
    )

    content_string = ''.join(data.astype(str))

    return content_string


def create_file(path, config):
    """Створює текстовий файл з контрольованим вмістом."""
    try:
        content = generate_numpy_content(config["MIN_FILE_SIZE"], config["MAX_FILE_SIZE"])
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(f"Помилка при створенні файлу {path}: {e}")


def create_controlled_structure(base_path, config, current_depth=0):
    """
    Рекурсивно створює структуру директорій та файлів з передбачуваними параметрами.
    """

    #  Створення файлів на поточному рівні
    name_length = config["NAME_LENGTH"]

    for i in range(config["FILES_PER_LEVEL"]):
        file_name = f"file_{current_depth}_{i}_{generate_random_name(name_length)}.txt"
        file_path = os.path.join(base_path, file_name)
        create_file(file_path, config)

    #  Перевірка умови зупинки рекурсії
    if current_depth >= config["MAX_DEPTH"]:
        return

    #  Створення директорій та рекурсивний виклик
    for i in range(config["DIRS_PER_LEVEL"]):
        # Директорії мають унікальний префікс та випадкову частину назви
        dir_name = f"dir_{current_depth}_{i}_{generate_random_name(name_length)}"
        new_dir_path = os.path.join(base_path, dir_name)

        try:
            os.makedirs(new_dir_path)

            # Рекурсивний виклик для наступного рівня
            create_controlled_structure(new_dir_path, config, current_depth + 1)
        except Exception as e:
            print(f"Помилка при створенні директорії {new_dir_path}: {e}")


def create_tree_and_run(config):
    """
    Створює кореневу директорію, запускає генерацію та виводить статистику.
    """
    root_name = config["ROOT_NAME"]

    # Розрахунок приблизної кількості директорій
    num_dirs_total = 0
    d_per_l = config["DIRS_PER_LEVEL"]
    max_d = config["MAX_DEPTH"]

    for d in range(max_d + 1):
        num_dirs_total += d_per_l ** d

    total_files_estimate = num_dirs_total * config["FILES_PER_LEVEL"]

    print("--- Запуск створення контрольованої структури ---")
    print(f"Коренева директорія: '{root_name}'")
    print(f"Глибина: {max_d}")
    print(f"Усього очікуваних папок: {num_dirs_total}")
    print(f"Усього очікуваних файлів: {total_files_estimate}")
    print(f"Розмір файлів: {config['MIN_FILE_SIZE']} - {config['MAX_FILE_SIZE']} символів.")

    # Створення кореневої директорії
    if os.path.exists(root_name):
        print(
            f"Попередження: Директорія '{root_name}' вже існує.")
    else:
        os.makedirs(root_name)
        print(f"Створено кореневу директорію.")

    # Запуск рекурсії
    create_controlled_structure(root_name, config, current_depth=0)

    print("Створення завершено! ")


# Приклад Використання

def generate_files(dir_: str):
    print("Асинхронна версія ефективна тільки для великих файлів, для малих вона втрачає сенс. "
          "Але генерація великих файлів займає багато часу.\n Для демострації ефективності (довго генерується) "
          "введіть:\nMIN_FILE_SIZE: 1000000, "
          "MAX_FILE_SIZE: 10000000,\n Для простого тесту використайте MIN_FILE_SIZE: 1, "
          "MAX_FILE_SIZE: 1000,")
    BIG_LOAD_CONFIG = {
        "ROOT_NAME": dir_ or "data",
        "MAX_DEPTH": 3,
        "DIRS_PER_LEVEL": 2,
        "FILES_PER_LEVEL": 3,
        "MIN_FILE_SIZE": int(input("MIN_FILE_SIZE:")),
        "MAX_FILE_SIZE": int(input("MAX_FILE_SIZE:")),
        "NAME_LENGTH": 8
    }
    create_tree_and_run(BIG_LOAD_CONFIG)

    print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    generate_files()
