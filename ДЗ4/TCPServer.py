import socket

def tcp_server():
    port = 12345  # Порт, на якому працює сервер

    try:
        # Запуск сервера
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(('0.0.0.0', port))
            server_socket.listen()
            print("Сервер запущено, очікування підключення...")

            while True:
                # Очікування підключення клієнта
                client_socket, client_address = server_socket.accept()
                print(f"Підключено клієнта: {client_address}")

                # Обробка повідомлень
                with client_socket:
                    message = client_socket.recv(1024).decode('utf-8')
                    print(f"Отримано повідомлення: {message}")

                    # Відповідь клієнту
                    response = f"Сервер отримав ваше повідомлення: {message}"
                    client_socket.sendall(response.encode('utf-8'))
                    print("Відповідь надіслано.")

    except Exception as e:
        print(f"Помилка сервера: {e}")

if __name__ == "__main__":
    tcp_server()

