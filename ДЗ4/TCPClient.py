import socket

def tcp_client():
    server_address = 'localhost'  # Адреса сервера
    port = 12345  # Порт сервера

    try:
        # Підключення до сервера
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((server_address, port))
            print("Успішно підключено до сервера.")

            # Відправлення повідомлення серверу
            message = "Привіт. Отримав повідомлення?"
            client_socket.sendall(message.encode('utf-8'))
            print(f"Надіслано повідомлення: {message}")

            # Отримання відповіді від сервера
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Відповідь від сервера: {response}")

    except Exception as e:
        print(f"Помилка клієнта: {e}")

if __name__ == "__main__":
    tcp_client()
