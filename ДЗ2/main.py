import concurrent.futures
import queue

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

# Функція для обробки черги чисел
def process_numbers(numbers_queue, results_queue):
    while not numbers_queue.empty():
        try:
            number = numbers_queue.get_nowait()  # Витягуємо число з черги
            steps = collatz_steps(number)        # Обчислюємо кроки
            results_queue.put(steps)             # Додаємо результат до черги результатів
        except queue.Empty:
            break

# Основна програма
if __name__ == "__main__":
    NUMBERS = 10_000_000
    THREADS = 8

    # Створюємо черги
    numbers_queue = queue.Queue()
    results_queue = queue.Queue()

    # Заповнюємо чергу числами
    for i in range(1, NUMBERS + 1):
        numbers_queue.put(i)

    # Використовуємо ThreadPoolExecutor для створення пулу потоків
    with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = [executor.submit(process_numbers, numbers_queue, results_queue) for _ in range(THREADS)]

    # Очікуємо завершення всіх потоків
    concurrent.futures.wait(futures)

    # Підрахунок середньої кількості кроків
    total_steps = 0
    count = 0
    while not results_queue.empty():
        total_steps += results_queue.get()
        count += 1

    average_steps = total_steps / count if count else 0
    print(f"Середня кількість кроків: {average_steps}")