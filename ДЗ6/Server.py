import socket
import struct

def server():
    host = '127.0.0.1'
    port = 65432
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Сервер слухає {host}:{port}...")

    conn, addr = server_socket.accept()
    print(f"З'єднання встановлено з {addr}")

    for _ in range(100):
        # Receive message length
        header = conn.recv(4)
        if not header:
            break
        message_length = struct.unpack('!I', header)[0]

        # Receive the actual message
        message = conn.recv(message_length).decode('utf-8')
        print(f"Сервер отримав: {message}")

        # Respond with acknowledgment
        response = f"ACK: {message}"
        response_encoded = response.encode('utf-8')
        response_length = struct.pack('!I', len(response_encoded))
        conn.sendall(response_length + response_encoded)

    conn.close()
    server_socket.close()

if __name__ == "__main__":
    server()
