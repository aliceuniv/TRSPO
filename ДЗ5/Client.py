import socket


def start_client():
    host = '127.0.0.1'  # Адреса сервера
    port = 65432  # Порт сервера

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    print(f"Підключено до сервера на {host}:{port}")

    while True:
        # Відправка повідомлення серверу
        message = input("Введіть повідомлення серверу: ")
        client_socket.send(message.encode())

        # Отримання відповіді від сервера
        data = client_socket.recv(1024).decode()
        if not data:
            break
        print(f"Сервер: {data}")

    client_socket.close()
    print("З'єднання закрито.")


if __name__ == "__main__":
    start_client()
