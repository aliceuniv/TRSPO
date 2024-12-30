import socket
import threading
import numpy as np
from concurrent.futures import ThreadPoolExecutor


# Функція для перевірки сумісності матриць для множення
def check_matrix_sizes(matrix_a, matrix_b):
    if matrix_a.shape[1] != matrix_b.shape[0]:
        raise ValueError(
            "Невірні розміри для множення матриць: кількість стовпців A має дорівнювати кількості рядків B")


# Функція для обчислення одного рядка результату
def compute_row(matrix_a, matrix_b, row_idx):
    return np.dot(matrix_a[row_idx], matrix_b)


def handle_client(connection, address):
    try:
        print(f"З'єднано з {address}")

        # Прийом розмірів матриць
        size_data = connection.recv(1024).decode()
        n, m, l = map(int, size_data.split())
        print(f"Отримано розміри: N={n}, M={m}, L={l}")

        # Прийом першої матриці
        matrix_a_data = connection.recv(n * m * 8)
        while len(matrix_a_data) < n * m * 8:
            matrix_a_data += connection.recv(n * m * 8 - len(matrix_a_data))
        matrix_a = np.frombuffer(matrix_a_data, dtype=np.float64).reshape((n, m))
        print(f"Отримано матрицю A розміром {matrix_a.shape}")

        # Прийом другої матриці
        matrix_b_data = connection.recv(m * l * 8)
        while len(matrix_b_data) < m * l * 8:
            matrix_b_data += connection.recv(m * l * 8 - len(matrix_b_data))
        matrix_b = np.frombuffer(matrix_b_data, dtype=np.float64).reshape((m, l))
        print(f"Отримано матрицю B розміром {matrix_b.shape}")

        # Перевірка сумісності розмірів матриць для множення
        check_matrix_sizes(matrix_a, matrix_b)

        # Використовуємо ThreadPoolExecutor для паралельного обчислення рядків результату
        with ThreadPoolExecutor() as executor:
            result_rows = list(executor.map(lambda row_idx: compute_row(matrix_a, matrix_b, row_idx), range(n)))

        # Перетворюємо список результатів на матрицю
        result = np.vstack(result_rows)
        print(f"Результуючий розмір {result.shape}")

        # Відправка результату клієнту
        connection.sendall(result.tobytes())
        print(f"Результат надіслано до {address}")

    except Exception as e:
        print(f"ERROR під'єнання {address}: {e}")
    finally:
        connection.close()


def start_server(host='127.0.0.1', port=12345):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print("Під'єнання серверу...")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    start_server()
