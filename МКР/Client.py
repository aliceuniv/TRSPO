import socket
import numpy as np
import random


def generate_matrix(rows, cols):
    return np.random.rand(rows, cols)


def client_program(host='127.0.0.1', port=12345):
    # Генерація випадкових розмірів та матриць
    n, m, l = random.randint(1001, 1100), random.randint(1001, 1100), random.randint(1001, 1100)
    matrix_a = generate_matrix(n, m)
    matrix_b = generate_matrix(m, l)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((host, port))
        print("Під'єднано до серверу")

        # Відправка розмірів
        client.sendall(f"{n} {m} {l}".encode())

        # Відправка матриць
        client.sendall(matrix_a.tobytes())
        client.sendall(matrix_b.tobytes())
        print("Матриця надіслана")

        # Отримання результату
        result_size = n * l * 8
        result_data = b""
        while len(result_data) < result_size:
            result_data += client.recv(result_size - len(result_data))
        result_matrix = np.frombuffer(result_data, dtype=np.float64).reshape((n, l))

        print("Отримано результат обчислення")
        print(result_matrix)


if __name__ == "__main__":
    client_program()
