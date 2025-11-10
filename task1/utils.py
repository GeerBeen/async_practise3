import numpy as np
import time
from typing import List, Tuple, Optional


def generate_array(rows: int, cols: int, low: int = 0, high: int = 10_000, seed: Optional[int] = None) -> np.ndarray:
    if seed is not None:
        np.random.seed(seed)
    return np.random.randint(low, high + 1, size=(rows, cols), dtype=np.int32)


def split_into_chunks(arr: np.ndarray, n_chunks: int) -> List[np.ndarray]:
    return np.array_split(arr, n_chunks, axis=0)


def search_in_chunk(chunk: np.ndarray, target: int) -> Optional[int]:
    mask = chunk >= target  # перевіряю чи є в чанку більше дорівнює
    if not mask.any():  # якщо нема, то нема
        return None
    return int(chunk[mask].min())  # якщо є, то повертає найменший з них


# отримує список результатів, знаходить найменше серед них
def combine_results(results: List[Optional[int]]) -> Optional[int]:
    valid = [r for r in results if r is not None]
    return min(valid) if valid else None


# декоратор для обрахунку часу виконання
def timed(fn):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        elapsed = time.perf_counter() - start
        return result, elapsed  # кожна функція з цим декоратором тепер повертає кортеж двох значень,
        # перше - результат виконання, друге - час виконання

    return wrapper


def read_input() -> Tuple[int, int, int, int]:
    while True:
        try:
            print("Введіть параметри масиву:")
            rows = int(input("  Кількість рядків: "))
            cols = int(input("  Кількість стовпців: "))
            if rows <= 0 or cols <= 0 or rows * cols < 1_000_000:
                print("Масив має бути > 0 і >= 1 000 000 елементів!")
                continue
            low = int(input("  Мінімальне значення: "))
            high = int(input("  Максимальне значення: "))
            if low > high:
                print("Мінімум не може бути більше максимуму!")
                continue
            return rows, cols, low, high
        except ValueError:
            print("Вводьте цілі числа!")
