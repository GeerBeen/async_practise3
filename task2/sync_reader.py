from utils import get_txt_files, timed, count_chars_in_file


@timed
def process_sync(directory: str):
    files = get_txt_files(directory)
    results = [count_chars_in_file(f) for f in files]
    return results


def run_sync(directory: str):
    return process_sync(directory)
