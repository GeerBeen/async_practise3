from work_stealing_files import run_work_stealing
from sync_reader import run_sync
import os
from generate_test_files import generate_files


def print_results(name, results, elapsed):
    total = sum(count for _, count in results)
    print(f"\n{name}:")
    print(f"   Файлів: {len(results)}")
    print(f"   Символів: {total:,}")
    print(f"   Час: {elapsed:.4f} с")


def main():
    directory = input("Введіть назву директорії для генерації (просто назва, enter для ./data): ") or "data"
    generate_files(directory)
    print("ПОРІВНЯННЯ: threads vs sync")
    print("=" * 60)

    if not os.path.isdir(directory):
        print("Директорія не існує")
        return

    # Threads
    print("Запуск ThreadPoolExecutor...")
    results_thread, time_thread = run_work_stealing(directory)
    print_results("THREADS", results_thread, time_thread)

    # Sync
    print("Запуск синхронно...")
    results_sync, time_sync = run_sync(directory)
    print_results("SYNC", results_sync, time_sync)

    # Підсумок
    print("\n" + "=" * 60)
    print("ПІДСУМОК:")
    times = {
        "threads": time_thread,
        "sync": time_sync
    }
    fastest = min(times, key=times.get)
    print(f"   Найшвидший: {fastest.upper()} — {times[fastest]:.4f} с")
    for name, t in times.items():
        if name != fastest:
            speedup = t / times[fastest]
            print(f"   {name.capitalize():8} повільніше у {speedup:.2f}×")


if __name__ == "__main__":
    main()
