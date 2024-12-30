import threading
import time

# Функція для першого потоку
def calculate_sum():
    print("Обчислення суми почалося...")
    result = sum(range(1_000_000))
    print(f"Сума чисел від 0 до 999,999: {result}")

# Функція для другого потоку
def calculate_factorial():
    print("Обчислення факторіалу почалося...")
    result = 1
    for i in range(1, 101):  # Обчислюємо факторіал 100
        result *= i
    print(f"Факторіал числа 100: {result}")

# Створюємо потоки
thread1 = threading.Thread(target=calculate_sum)
thread2 = threading.Thread(target=calculate_factorial)

# Запускаємо потоки
thread1.start()
thread2.start()

# Очікуємо завершення потоків
thread1.join()
thread2.join()

print("Усі обчислення завершені.")
