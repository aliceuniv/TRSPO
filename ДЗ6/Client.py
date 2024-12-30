import socket
import struct

def client():
    host = '127.0.0.1'
    port = 65432
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"З'єднано з сервером {host}:{port}")

    for i in range(100):
        # Create and send a message
        message = f"Повідомлення {i+1}"
        message_encoded = message.encode('utf-8')
        message_length = struct.pack('!I', len(message_encoded))
        client_socket.sendall(message_length + message_encoded)

        # Receive acknowledgment
        header = client_socket.recv(4)
        if not header:
            break
        response_length = struct.unpack('!I', header)[0]
        response = client_socket.recv(response_length).decode('utf-8')
        print(f"Клієнт отримав: {response}")

    client_socket.close()

if __name__ == "__main__":
    client()
