import socket
import threading
import json
from datetime import datetime

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000
BUFFER_SIZE = 1024

clients = {}
lock = threading.Lock()


def log(message):
    time_stamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{time_stamp}] {message}")


def send_json(sock, data):
    message = json.dumps(data) + "\n"
    sock.sendall(message.encode())


def broadcast_system(message):
    with lock:
        for sock in clients.values():
            send_json(sock, {
                "type": "system",
                "message": message
            })


def handle_client(client_socket, client_address):
    username = None
    try:
        username = client_socket.recv(BUFFER_SIZE).decode().strip()

        if not username:
            client_socket.close()
            return

        with lock:
            if username in clients:
                send_json(client_socket, {
                    "type": "error",
                    "message": "Username already taken."
                })
                client_socket.close()
                return

            clients[username] = client_socket

        log(f"{username} connected from {client_address}")

        send_json(client_socket, {
            "type": "system",
            "message": f"Welcome {username} to ClassChatX."
        })

        broadcast_system(f"{username} joined the chat.")

        buffer = ""

        while True:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break

            buffer += data.decode()

            while "\n" in buffer:
                message, buffer = buffer.split("\n", 1)

                try:
                    json_data = json.loads(message)
                except:
                    continue

                receiver = json_data.get("receiver")
                text = json_data.get("text")

                if not receiver or not text:
                    send_json(client_socket, {
                        "type": "error",
                        "message": "Invalid message format."
                    })
                    continue

                with lock:
                    if receiver in clients:
                        send_json(clients[receiver], {
                            "type": "chat",
                            "sender": username,
                            "text": text
                        })
                        log(f"{username} -> {receiver}: {text}")
                    else:
                        send_json(client_socket, {
                            "type": "error",
                            "message": f"User '{receiver}' not found."
                        })

    except Exception as e:
        log(f"Error with {username}: {e}")

    finally:
        if username:
            with lock:
                if username in clients:
                    del clients[username]
            broadcast_system(f"{username} left the chat.")
            log(f"{username} disconnected.")

        client_socket.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen()

    log(f"ClassChatX server running on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        thread = threading.Thread(
            target=handle_client,
            args=(client_socket, client_address)
        )
        thread.start()


if __name__ == "__main__":
    start_server()