from concurrent.futures import ThreadPoolExecutor
from Practise3.task1.utils import split_into_chunks, search_in_chunk, combine_results, timed
import os


@timed
def compute_stealing(arr, target, n_workers=None, tasks_per_worker=8):
    if n_workers is None:
        n_workers = os.cpu_count() or 8

    # Створюю більше чанків ніж кількість воркерів,
    # щоб було що красти потокам, які виконають свої чанки швидше за інших,
    # інакше при однаковій кількості чанків і потоків це буде аналогічно work dealing
    total_tasks = n_workers * tasks_per_worker
    chunks = split_into_chunks(arr, total_tasks)

    with ThreadPoolExecutor(max_workers=n_workers) as executor:
        # executor.map автоматично розподіляє чанки по потокам
        results = list(executor.map(search_in_chunk, chunks, [target] * len(chunks)))
    return combine_results(results)


def run_work_stealing(arr, target, n_workers=None):
    return compute_stealing(arr, target, n_workers, tasks_per_worker=8)
