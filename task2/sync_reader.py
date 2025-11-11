from utils import get_txt_files, timed


@timed
def process_sync(directory: str):
    files = get_txt_files(directory)
    results = []
    for f in files:
        try:
            content = f.read_text(encoding='utf-8', errors='ignore')
            results.append((f.name, len(content)))
        except Exception:
            results.append((f.name, 0))
    return results


def run_sync(directory: str):
    return process_sync(directory)
