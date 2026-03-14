import socket
import threading
from datetime import datetime

# Server configuration
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000
BUFFER_SIZE = 1024

# Logging function
def log(message):
    time_stamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{time_stamp}] {message}")

# Function to handle each client
def handle_client(client_socket, client_address):
    log(f"Client connected from {client_address}")

    # Send introduction message
    intro_message = (
        "Welcome to ClassChatX.\n"
        "I am the ClassChatX server. I manage client connections and forward messages between users.\n"
    )
    client_socket.sendall(intro_message.encode())

    try:
        while True:
            # Receive message from client
            message = client_socket.recv(BUFFER_SIZE)

            if not message:
                break

            decoded_message = message.decode()
            log(f"Message from {client_address}: {decoded_message}")

            # Send acknowledgement
            response = f"Server received: {decoded_message}"
            client_socket.sendall(response.encode())

    except Exception as e:
        log(f"Error with {client_address}: {e}")

    finally:
        client_socket.close()
        log(f"Connection closed for {client_address}")

# Start server
def start_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((SERVER_HOST, SERVER_PORT))

    server_socket.listen()

    log(f"ClassChatX server started on {SERVER_HOST}:{SERVER_PORT}")
    log("Waiting for client connections...")

    while True:
        client_socket, client_address = server_socket.accept()

        # Create a new thread for each client
        client_thread = threading.Thread(
            target=handle_client,
            args=(client_socket, client_address)
        )

        client_thread.start()

if __name__ == "__main__":
    start_server()
