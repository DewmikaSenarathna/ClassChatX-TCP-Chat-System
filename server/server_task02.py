import socket
import threading
from datetime import datetime

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000
BUFFER_SIZE = 1024

clients = []
client_names = {}


def log(message):
    time_stamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{time_stamp}] {message}")


def broadcast(message, sender_socket=None):
    for client in clients[:]:
        if client != sender_socket:
            try:
                client.sendall(message.encode())
            except:
                if client in clients:
                    clients.remove(client)
                if client in client_names:
                    del client_names[client]
                client.close()


def handle_client(client_socket, client_address):
    try:
        # Ask client name
        client_socket.sendall("Enter your name: ".encode())
        name = client_socket.recv(BUFFER_SIZE).decode().strip()

        if not name:
            name = f"{client_address[0]}:{client_address[1]}"

        client_names[client_socket] = name
        log(f"{name} joined from {client_address}")

        welcome_message = f"Welcome {name}! You can now start chatting.\n"
        client_socket.sendall(welcome_message.encode())

        broadcast(f"[SERVER] {name} has joined the chat.\n", client_socket)

        while True:
            message = client_socket.recv(BUFFER_SIZE).decode()

            if not message:
                break

            message = message.strip()

            if message.lower() == "exit":
                break

            full_message = f"{name}: {message}\n"
            log(full_message.strip())
            broadcast(full_message, client_socket)

    except Exception as e:
        log(f"Error with client {client_address}: {e}")

    finally:
        if client_socket in clients:
            clients.remove(client_socket)

        name = client_names.get(client_socket, f"{client_address[0]}:{client_address[1]}")
        if client_socket in client_names:
            del client_names[client_socket]

        log(f"{name} disconnected.")
        broadcast(f"[SERVER] {name} has left the chat.\n", client_socket)

        client_socket.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)

    log(f"ClassChatX Task 02 server started on {SERVER_HOST}:{SERVER_PORT}")
    log("Waiting for client connections...")

    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)

        client_thread = threading.Thread(
            target=handle_client,
            args=(client_socket, client_address)
        )
        client_thread.start()


if __name__ == "__main__":
    start_server()
