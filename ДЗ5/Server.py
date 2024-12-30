import socket


def start_server():
    host = '127.0.0.1'  # Локальний хост
    port = 65432  # Порт для прослуховування

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Сервер чекає на з'єднання на {host}:{port}...")
    conn, addr = server_socket.accept()
    print(f"З'єднання встановлено з {addr}")

    while True:
        # Отримання повідомлення від клієнта
        data = conn.recv(1024).decode()
        if not data:
            break
        print(f"Клієнт: {data}")

        # Відправка відповіді клієнту
        response = input("Введіть відповідь: ")
        conn.send(response.encode())

    conn.close()
    print("З'єднання закрито.")


if __name__ == "__main__":
    start_server()
