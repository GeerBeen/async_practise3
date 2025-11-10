from pathlib import Path
from typing import List, Tuple
import time


def timed(fn):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        elapsed = time.perf_counter() - start
        return result, elapsed

    return wrapper


def get_txt_files(directory: str) -> List[Path]:
    #  отримує шляхи до текстових файлів з директорій
    path = Path(directory)
    if not path.exists():
        raise ValueError(f"Директорія не існує: {directory}")
    if not path.is_dir():
        raise ValueError(f"Це не директорія: {directory}")
    return sorted(path.rglob("*.txt"))


def count_chars_in_file(filepath: Path) -> Tuple[str, int]:
    #  Читає файл, повертає ім'я і кількість символів
    try:
        content = filepath.read_text(encoding='utf-8', errors='ignore')
        return filepath.name, len(content)
    except Exception as e:
        return filepath.name, 0


def print_results(results: List[Tuple[str, int]]):
    total = 0
    print("\nРезультати:")
    print("-" * 50)
    for name, count in results:
        print(f"{name}: {count:,} символів")
        total += count
    print("-" * 50)
    print(f"Всього символів: {total:,}")
