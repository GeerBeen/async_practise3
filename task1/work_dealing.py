from concurrent.futures import ThreadPoolExecutor, as_completed
from Practise3.task1.utils import split_into_chunks, search_in_chunk, combine_results, timed
import os


@timed
def compute_dealing(arr, target, n_workers=None):
    if n_workers is None:
        n_workers = os.cpu_count()
    chunks = split_into_chunks(arr, n_workers)  # розбиваю масив на чанки
    with ThreadPoolExecutor(max_workers=n_workers) as executor:
        # з executor.submit кожному потоку задаю свій чанк вручну
        # створюю об'єкти фьючів з кожного потоку
        futures = [executor.submit(search_in_chunk, chunk, target) for chunk in chunks]
        # отримую результати фьючів коли вони стають закінчені
        results = [f.result() for f in as_completed(futures)]
    return combine_results(results)


def run_work_dealing(arr, target, n_workers=None):
    return compute_dealing(arr, target, n_workers)
