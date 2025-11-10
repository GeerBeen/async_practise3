# work_stealing_files.py
from concurrent.futures import ThreadPoolExecutor
from utils import get_txt_files, count_chars_in_file, timed
import os


@timed
def process_files_stealing(directory: str, n_workers=None) -> list:
    if n_workers is None:
        n_workers = os.cpu_count() or 8

    files = get_txt_files(directory)
    if not files:
        return []

    with ThreadPoolExecutor(max_workers=n_workers) as executor:
        # count_chars_in_file викликається і потік займається
        results = list(executor.map(count_chars_in_file, files))

    return results


def run_work_stealing(directory: str, n_workers=None):
    results, elapsed = process_files_stealing(directory, n_workers)
    return results, elapsed
