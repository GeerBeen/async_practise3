import random

from utils import generate_array, read_input
from work_stealing import run_work_stealing
from work_dealing import run_work_dealing
from work_sync import work_sync


def main():
    # Умова задачі побудована таким чином, що часто 2*(перше значення масиву) - таргет, буде більшим
    # за його максимальне значення, тобто вийде так, що мінімальне значення удвічі більше
    # за перше не знайдеться ніколи. Я вирішив що буду ігнорувати цю проблему і просто шукати його,
    # адже час виконання для мене головніше ніж знаходження числа якого немає.
    #
    SEED = 63872  # сід за якого таргет значення можна було знайти (мінімально наближене до таргету при такх параметрах #rows, cols, low, high = 1000, 1000, 0, 9999999)
    # SEED = None
    # print(SEED)
    print("=== Практична: Варіант 3 ===")

    rows, cols, low, high = read_input()
    # rows, cols, low, high = 1000, 1000, 0, 9999999

    arr = generate_array(rows, cols, low, high, SEED)

    print("Згенерований масив:\n", arr)
    print(f"Перший елемент: {arr.flat[0]} → шукаємо: {arr.flat[0] * 2}\n")

    target = arr.flat[0] * 2
    if target >= high:
        print("Подвоєне значення першого елементу масиву більше за максимальне значення масиву, "
              "а отже воно ніколи не буде знайдено!\nАле я продовжую пошук, бо час порівняння для мене головне")

    n_workers = 8

    print("Запуск обчислень...\n")

    # Work Stealing
    print("1. Work Stealing (ThreadPoolExecutor + map)")
    result_ws, time_ws = run_work_stealing(arr, target, n_workers)
    print(f"   Результат: {result_ws or 'не знайдено'}")
    print(f"   Час: {time_ws:.4f} сек\n")

    # Work Dealing
    print("2. Work Dealing (ThreadPoolExecutor + submit)")
    result_wd, time_wd = run_work_dealing(arr, target, n_workers)
    print(f"   Результат: {result_wd or 'не знайдено'}")
    print(f"   Час: {time_wd:.4f} сек\n")

    # Work Sync
    print("3. Work Sync (Чистий numpy)")
    result_wsn, time_wsn = run_work_dealing(arr, target)
    print(f"   Результат: {result_wsn or 'не знайдено'}")
    print(f"   Час: {time_wsn:.4f} сек\n")

    # Порівняння
    print("=" * 60)
    print("ПІДСУМОК:")
    print(f"   Work Stealing : {time_ws:.4f} с → {result_ws}")
    print(f"   Work Dealing  : {time_wd:.4f} с → {result_wd}")
    print(f"   Work Sync     : {time_wsn:.4f} с → {result_wsn}")

    # Знаходимо найшвидший варіант
    times = {
        "Work Stealing": time_ws,
        "Work Dealing": time_wd,
        "Work Sync": time_wsn
    }

    fastest_name = min(times, key=times.get)
    fastest_time = times[fastest_name]

    if fastest_name == "Work Sync":
        print(f"   Найшвидший: {fastest_name} — {fastest_time:.4f} с")
    else:
        speedup = time_wsn / fastest_time
        print(f"   Найшвидший: {fastest_name} — {fastest_time:.4f} с")
        print(f"   Прискорення відносно Sync: {speedup:.2f}x")

    if time_ws < time_wd:
        print(f"   Stealing швидший за Dealing на {time_wd - time_ws:.4f} с")
    else:
        print(f"   Dealing швидший за Stealing на {time_ws - time_wd:.4f} с")


if __name__ == "__main__":
    main()
