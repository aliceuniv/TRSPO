import concurrent.futures
import threading

# Функція для обчислення кількості кроків відповідно до гіпотези Колаца
def collatz_steps(n):
    steps = 0
    while n > 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        steps += 1
    return steps

# Глобальні змінні для збереження загальних кроків і кількості обчислених чисел
total_steps = 0
total_count = 0
total_steps_lock = threading.Lock()
total_count_lock = threading.Lock()

# Функція для обробки чисел
def process_numbers(numbers_range):
    global total_steps, total_count
    local_steps = 0
    local_count = 0

    for number in numbers_range:
        local_steps += collatz_steps(number)
        local_count += 1

    # Атомарне оновлення глобальних змінних
    with total_steps_lock:
        total_steps += local_steps
    with total_count_lock:
        total_count += local_count

# Основна програма
if __name__ == "__main__":
    NUMBERS = 10_000_000
    THREADS = 8

    # Розбиваємо числа на частини для потоків
    chunk_size = NUMBERS // THREADS
    ranges = [range(i * chunk_size + 1, (i + 1) * chunk_size + 1) for i in range(THREADS)]
    if NUMBERS % THREADS:
        ranges[-1] = range((THREADS - 1) * chunk_size + 1, NUMBERS + 1)

    # Використовуємо ThreadPoolExecutor для створення пулу потоків
    with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as executor:
        executor.map(process_numbers, ranges)

    # Обчислюємо середню кількість кроків
    average_steps = total_steps / total_count if total_count else 0
    print(f"Середня кількість кроків: {average_steps}")
